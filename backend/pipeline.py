import pandas as pd
import numpy as np
import re
import os

from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
 
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from llama_cpp import Llama
from langgraph.graph import END

# =========================
# 🔴 LOAD MODELS (FIXED PATHS)
# =========================

llm_type = Llama(
    model_path="../models/mistral.Q4_K_M.gguf",
    n_ctx=4096,
    n_gpu_layers=20,
    n_threads=4
)

llm_priority = Llama(
    model_path="../models/mistral.Q4_K_M.gguf",
    n_ctx=4096,
    n_gpu_layers=15,
    n_threads=4
)

llm_queue = LlamaCpp(
    model_path="../models/llama-2-7b-chat.Q4_K_M.gguf",
    temperature=0,
    max_tokens=20,
    n_ctx=4096,
    n_gpu_layers=25
)

llm_response = LlamaCpp(
    model_path="../models/mistral.Q4_K_M.gguf",
    temperature=0.4,
    max_tokens=200,
    n_ctx=4096,
    n_gpu_layers=20
)

# ---------------------------
# Load dataset
# ---------------------------
df = pd.read_csv("../data/dataset_raw_400.csv")

# ---------------------------
# Cleaning function
# ---------------------------
def clean_ticket(text):

    if text is None:
        return ""

    text = text.lower()

    # remove urls
    text = re.sub(r"http\S+|www\S+", "", text)

    # remove greetings
    greetings = [
        "dear customer support team",
        "dear support team",
        "dear team",
        
        "dear sir",
        "dear madam",
        "hello",
        "hi",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    for g in greetings:
        text = text.replace(g, "")

    # remove signatures
    signatures = [
        "thanks",
        "thank you",
        "regards",
        "best regards",
        "kind regards",
        "sincerely",
        "yours sincerely"
    ]

    for s in signatures:
        text = text.replace(s, "")

    # remove newline characters
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")

    # remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ---------------------------
# Filter dataset
# ---------------------------
df = df[df["language"] == "en"]

df = df.dropna(subset=[
    "subject", "body", "type", "priority", "queue","answer"
])

df = df[["subject", "body", "type", "priority", "queue", "answer"]]

# ---------------------------
# Create ticket text
# ---------------------------
df["ticket_text"] = df["subject"].astype(str) + " " + df["body"].astype(str)

df["ticket_text"] = df["ticket_text"].apply(clean_ticket)

# ---------------------------
# Normalize labels (VERY IMPORTANT)
# ---------------------------
df["type"] = df["type"].str.strip().str.title()
df["priority"] = df["priority"].str.strip().str.title()
df["queue"] = df["queue"].str.strip()

# ---------------------------
# Final check
# ---------------------------


def build_prompt10(ticket_text):

    instruction = f"""
You are an IT Service Management classifier.

Classify the following ticket into ONE category:

Incident
Problem
Request
Change


Definitions:

Incident:
A ticket reporting a system failure, crash, outage,
security breach, unauthorized access, or malfunction
that disrupts a service or application.

These tickets usually describe events such as:
system crashes, service outages, login failures,
data breaches, software malfunctions, or tools
suddenly stopping working.

Examples include:
software crashes, login errors, system outages, data breaches,
tools not working, service disruptions.


Problem:
A ticket describing system performance issues,
data inconsistencies, analytics inaccuracies,
integration difficulties, or operational inefficiencies.

These tickets usually involve situations such as:
slow performance, incorrect analytics results,
data synchronization problems, integration issues,
forecasting errors, or system behavior that is not
working correctly but is not a sudden crash or outage.


Request:
A ticket where the user is asking for information, documentation,
guidance, instructions, pricing details, or help understanding
features or services.

The user is NOT reporting a malfunction.

Examples include asking for:
integration guides, pricing information, documentation,
security best practices, or configuration instructions.


Change:
A ticket requesting a modification, upgrade, improvement,
optimization, or implementation of new functionality in a
system, configuration, integration, billing setup, or security
policy.

The system is generally working but needs improvement or updates.

Examples include:
upgrading integrations, improving security protocols,
enhancing user interfaces, adding new analytics tools,
or adjusting billing settings.



Decision rule:

If the ticket describes a sudden failure,
crash, outage, security breach, or tool not
working → Incident.

If the ticket describes slow performance,
incorrect results, recurring issues, or
integration problems → Problem.

If the user is asking for information
or guidance → Request.

If the user wants to modify or improve
a system → Change.


Respond with ONLY one word:
Incident, Problem, Request, or Change.


Ticket:
{ticket_text}
"""

    return f"<s>[INST] {instruction} [/INST]"


allowed_labels = ["Incident", "Problem", "Request", "Change"]

def predict_type10(ticket_text):

    prompt = build_prompt10(ticket_text)

    output = llm_type(
        prompt,
        max_tokens=4,
        temperature=0,
        stop=["\n"]
    )

    response = output["choices"][0]["text"].strip()

    for label in allowed_labels:
        if re.search(r'\b' + label + r'\b', response, re.IGNORECASE):
            return label

    return "ParsingError"

def build_priority_prompt4(ticket_text, ticket_type):

    instruction = f"""
You are an expert IT Service Management (ITSM) priority classifier.

Each support ticket must be assigned a PRIORITY level based on
how severe the issue is and how much it affects operations.

Possible priorities:

High
Medium
Low


Ticket Type:
{ticket_type}


Understand the difference between the priorities carefully.


HIGH PRIORITY

A ticket should be classified as High when the problem
causes a major disruption, system outage, security risk,
or prevents users from performing essential tasks.

Typical situations include:

• System or application crashes
• Service outages or platforms being unavailable
• Users unable to access important systems
• Security breaches or unauthorized access
• Multiple devices or services failing
• Issues severely disrupting business operations

Examples:

- "The SaaS platform is offline and users cannot log in."
- "Critical security breach exposing patient data."
- "Employees cannot open Excel or PowerPoint across all devices."
- "Multiple core systems are failing and operations are blocked."

These issues require urgent attention because they
prevent normal business operations.



MEDIUM PRIORITY

A ticket should be classified as Medium when the system
is still functioning but has problems that affect productivity
or workflow.

The issue causes inconvenience or degraded performance,
but the service is still available.

Typical situations include:

• Network connectivity problems
• Intermittent access to systems
• Performance degradation
• Integration issues between systems
• Billing inconsistencies
• Workflow disruptions

Examples:

- "VPN connectivity issues affecting remote work."
- "Network connection keeps dropping intermittently."
- "Billing system shows inconsistent payment records."
- "Device connectivity problems across the office."

These issues impact productivity but do not completely
stop the system from functioning.



LOW PRIORITY

A ticket should be classified as Low when the request is
informational, non-urgent, or related to minor assistance.

These tickets typically ask for guidance, documentation,
or clarification rather than reporting a serious problem.

Typical situations include:

• Request for documentation
• Request for configuration guidance
• Questions about billing procedures
• Inquiries about services or products
• Minor single-device issues

Examples:

- "Request for CI/CD pipeline documentation."
- "Inquiry about marketing services."
- "Request for billing procedure details."
- "Question about investment strategies."

These tickets do not disrupt system operations
and therefore have low urgency.



IMPORTANT DECISION PROCESS

Before deciding the priority, think about these questions:

1. Does the issue stop users from accessing critical systems?
→ High

2. Does the system still work but with problems affecting workflow?
→ Medium

3. Is the ticket mainly asking for information or guidance?
→ Low



Classification Instructions:

Carefully read the ticket.
Determine how severely the issue affects operations.
Then output the correct priority.


Respond with ONLY one word:

high
medium
low



Ticket:
{ticket_text}

Priority:
"""

    return f"<s>[INST] {instruction} [/INST]"

def predict_priority4(ticket_text, ticket_type):

    prompt = build_priority_prompt4(ticket_text, ticket_type)

    output = llm_priority(
        prompt,
        max_tokens=5,
        temperature=0,
        stop=["\n"]
    )

    response = output["choices"][0]["text"].strip()

    allowed = ["high", "medium", "low"]

    for p in allowed:
        if p.lower() in response.lower():
            return p

    return "ParsingError"

from langchain.prompts import PromptTemplate

queue_prompt = PromptTemplate(
    input_variables=["ticket_text", "ticket_type", "priority", "examples"],
    template="""
You are an expert support ticket routing assistant.

Your task is to assign the correct queue based on meaning, not keywords.

Queue definitions:

- Billing and Payments → invoices, charges, payments, pricing issues
- Customer Service → general help, guidance, non-technical questions
- General Inquiry → broad questions not fitting any category
- Human Resources → employee-related or HR issues
- IT Support → hardware, system, device, OS, login issues
- Product Support → specific product/device malfunction or usage issue
- Returns and Exchanges → product return, refund, exchange requests
- Sales and Pre-Sales → pricing, plans, product inquiries before purchase
- Service Outages and Maintenance → system-wide outages, downtime, disruptions
- Technical Support → software, platform, API, SaaS, system errors

Below are similar tickets from the system:

{examples}

Now classify the following ticket.

Ticket: {ticket_text}
Type: {ticket_type}
Priority: {priority}

Return ONLY one exact queue name from the list above.
Do not explain.

Answer:
"""
)

from langchain.chains import LLMChain

queue_chain = LLMChain(
    llm=llm_queue,
    prompt=queue_prompt
)


train_df = pd.read_csv(
    "../data/hf_dataset_final_train.csv"
)

# keep only English
train_df = train_df[train_df["language"] == "en"]

# drop nulls
train_df = train_df.dropna(subset=[
    "subject", "body", "type", "priority", "queue", "answer"
])

# create ticket text
train_df["ticket_text"] = (
    train_df["subject"].astype(str) + " " +
    train_df["body"].astype(str)
)

train_df["ticket_text"] = train_df["ticket_text"].apply(clean_ticket)

for col in ["type", "priority", "queue"]:
    train_df[col] = train_df[col].str.strip().str.title()

queue_labels = sorted(train_df["queue"].unique())

test_df = pd.read_csv("../data/dataset_raw_400.csv")

test_df = test_df[test_df["language"] == "en"]

test_df = test_df.dropna(subset=[
    "subject", "body", "type", "priority", "queue","answer"
])

test_df = test_df[["subject", "body", "type", "priority", "queue", "answer"]]

# Create ticket text
test_df["ticket_text"] = (
    test_df["subject"].astype(str) + " " +
    test_df["body"].astype(str)
)

test_df["ticket_text"] = test_df["ticket_text"].apply(clean_ticket)


# ---------------------------
# NORMALIZE LABELS (VERY IMPORTANT)
# ---------------------------
for col in ["type", "priority", "queue"]:
    test_df[col] = test_df[col].str.strip().str.title()



def predict_queue3(ticket_text, ticket_type, priority):

    # 🔍 use correct retriever
    docs = queue_retriever.get_relevant_documents(ticket_text)

    examples_text = ""

    for doc in docs:
        meta = doc.metadata

        examples_text += f"""
Ticket: {doc.page_content[:250]}
Type: {meta['type']}
Priority: {meta['priority']}
Queue: {meta['queue']}
"""

    # 🔥 LLM call
    response = queue_chain.run(
        ticket_text=ticket_text[:400],
        ticket_type=ticket_type,
        priority=priority,
        examples=examples_text
    )

    response = response.strip()

    response_clean = response.lower()

    for q in queue_labels:
        if q.lower() == response_clean:
            return q

    for q in queue_labels:
        if q.lower() in response_clean:
            return q

    return "ParsingError"

from langchain.schema import Document

docs = []

for _, row in train_df.iterrows():

    if pd.isna(row["answer"]):
        continue

    docs.append(
        Document(
            page_content=row["ticket_text"],   # ONLY ticket text embedded
            metadata={
                "answer": row["answer"],
                "type": row["type"],
                "priority": row["priority"],
                "queue": row["queue"]
            }
        )
    )
response_prompt = PromptTemplate(
    input_variables=["ticket_text", "few_shot_examples"],
    template="""
You are a professional IT support assistant.

Study the examples carefully.

From the examples, learn:
- how the response is structured
- how tone changes (urgent, informational, etc.)
- what type of information is requested
- how the issue is acknowledged and handled

Examples:
{few_shot_examples}

Now respond to the new ticket.

Ticket:
{ticket_text}

Instructions:
- Follow the SAME structure as examples
- Match tone appropriately
- Keep response concise (4–6 lines)
- Avoid overly formal phrases
- Include all relevant details from the ticket
- Ensure the response directly answers the user's question


Response:
"""
)

def get_few_shot_examples(ticket_text, k=3):

    docs = response_retriever.get_relevant_documents(ticket_text)

    selected = []
    seen = set()

    for doc in docs:
        ans = doc.metadata["answer"]

        if pd.isna(ans):
            continue

        if ans not in seen:
            selected.append(ans)
            seen.add(ans)

        if len(selected) == k:
            break

    text = ""
    for i, ans in enumerate(selected, 1):
        text += f"Example {i}:\n{ans}\n\n"

    return text
response_chain = LLMChain(
    llm=llm_response,
    prompt=response_prompt
)
# 🔵 Shared embeddings (good)

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# 🟢 Queue vectorstore
queue_vectorstore = FAISS.from_texts(
    texts=train_df["ticket_text"].tolist(),
    metadatas=train_df[["type", "priority", "queue"]].to_dict("records"),
    embedding=embeddings
)

queue_retriever = queue_vectorstore.as_retriever(search_kwargs={"k": 5})


# 🔵 Response vectorstore
response_vectorstore = FAISS.from_documents(
    docs,
    embeddings
)

response_retriever = response_vectorstore.as_retriever(search_kwargs={"k": 10})

def response_node(state):

    ticket_text = state["ticket_text"]

    # 🔥 semantic few-shot (LangChain retriever)
    few_shot_examples = get_few_shot_examples(ticket_text)

    response = response_chain.run(
        ticket_text=ticket_text,
        few_shot_examples=few_shot_examples
    )

    return {
        **state,
        "response": response.strip()
    }

class TicketState(TypedDict):
    ticket_text: str
    type: str
    priority: str
    queue: str
    response: str 

def type_node(state):
    pred_type = predict_type10(state["ticket_text"])
    return {**state, "type": pred_type}


def priority_node(state):
    pred_priority = predict_priority4(
        state["ticket_text"],
        state["type"]
    )
    return {**state, "priority": pred_priority}


def queue_node(state):
    pred_queue = predict_queue3(
        state["ticket_text"],
        state["type"],
        state["priority"]
    )
    return {**state, "queue": pred_queue}



graph = StateGraph(TicketState)

graph.add_node("type_agent", type_node)
graph.add_node("priority_agent", priority_node)
graph.add_node("queue_agent", queue_node)
graph.add_node("response_agent", response_node)

graph.add_edge(START, "type_agent")

graph.add_edge("type_agent", "priority_agent")

graph.add_edge("priority_agent", "queue_agent")

graph.add_edge("queue_agent", "response_agent")

graph.add_edge("response_agent", END)

app = graph.compile()
