import re

print("Loading AmoebaTronix answer generator...")

# This answer generator uses the retrieved company knowledge
# and extracts the relevant answer without inventing information.


def clean_text(text):
    """Clean unnecessary spaces from retrieved knowledge."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def find_answer_in_context(question, context):
    """
    Find the most relevant FAQ answer from the retrieved
    AmoebaTronix knowledge.
    """

    question_clean = clean_text(question).lower()
    context_clean = clean_text(context)

    # Convert the knowledge base into individual sentences.
    sentences = re.split(r"(?<=[.!?])\s+", context_clean)

    # Important keywords for common AmoebaTronix questions.
    keyword_groups = {
        "it services": [
            "it services",
            "it infrastructure",
            "networking",
            "security",
            "hardware support",
            "amc",
            "facility management services"
        ],

        "software": [
            "custom software",
            "web applications",
            "apis",
            "business systems"
        ],

        "cloud": [
            "cloud solutions",
            "google workspace",
            "microsoft azure",
            "cloud backup",
            "virtual infrastructure"
        ],

        "products": [
            "it products",
            "servers",
            "workstations",
            "business laptops",
            "network printers"
        ],

        "licences": [
            "software licences",
            "windows",
            "windows server",
            "microsoft 365",
            "microsoft office"
        ],

        "events": [
            "event services",
            "corporate-event support",
            "stage and set design",
            "led walls",
            "lighting",
            "audio-visual production"
        ],

        "contact": [
            "contact",
            "phone",
            "email"
        ],

        "location": [
            "located",
            "headquarters",
            "address"
        ],

        "business hours": [
            "business hours",
            "hours",
            "timing"
        ]
    }

    # Detect the user's topic.
    selected_topic = None

    if any(word in question_clean for word in [
        "it service",
        "it services",
        "infrastructure",
        "networking",
        "hardware support",
        "amc",
        "fms"
    ]):
        selected_topic = "it services"

    elif any(word in question_clean for word in [
        "custom software",
        "software development",
        "web application",
        "api",
        "erp",
        "crm"
    ]):
        selected_topic = "software"

    elif any(word in question_clean for word in [
        "cloud",
        "google workspace",
        "azure"
    ]):
        selected_topic = "cloud"

    elif any(word in question_clean for word in [
        "product",
        "server",
        "laptop",
        "printer",
        "ups",
        "router",
        "switch"
    ]):
        selected_topic = "products"

    elif any(word in question_clean for word in [
        "licence",
        "license",
        "windows",
        "microsoft 365",
        "office"
    ]):
        selected_topic = "licences"

    elif any(word in question_clean for word in [
        "event",
        "stage",
        "led wall",
        "lighting",
        "audio",
        "mascot",
        "360"
    ]):
        selected_topic = "events"

    elif any(word in question_clean for word in [
        "contact",
        "phone",
        "email",
        "call"
    ]):
        selected_topic = "contact"

    elif any(word in question_clean for word in [
        "where",
        "location",
        "address",
        "headquarters"
    ]):
        selected_topic = "location"

    elif any(word in question_clean for word in [
        "hours",
        "timing",
        "open"
    ]):
        selected_topic = "business hours"

    # If we know the topic, find useful sentences.
    if selected_topic:

        keywords = keyword_groups[selected_topic]

        matched = []

        for sentence in sentences:
            sentence_lower = sentence.lower()

            score = sum(
                1 for keyword in keywords
                if keyword in sentence_lower
            )

            if score > 0:
                matched.append((score, sentence))

        if matched:
            matched.sort(
                key=lambda item: item[0],
                reverse=True
            )

            # Return the best relevant sentence(s).
            answer_sentences = [
                item[1] for item in matched[:3]
            ]

            return " ".join(answer_sentences)

    # Generic fallback.
    return (
        "I can help with AmoebaTronix IT services, software "
        "development, cloud solutions, products, licences, "
        "and event services. Please describe what you need."
    )


def generate_answer(question, context):
    """
    Generate a grounded answer using ONLY retrieved
    AmoebaTronix knowledge.
    """

    if not question.strip():
        return "Please enter a question."

    if not context.strip():
        return (
            "I could not find relevant information in the "
            "AmoebaTronix knowledge base."
        )

    answer = find_answer_in_context(
        question,
        context
    )

    return answer.strip()


if __name__ == "__main__":

    question = "What IT services do you provide?"

    context = """
    What IT services do you provide?
    We provide IT infrastructure, networking, security,
    hardware support, AMC, Facility Management Services,
    remote support, on-site support, and IT management.
    """

    answer = generate_answer(
        question,
        context
    )

    print("\n==============================")
    print("QUESTION")
    print("==============================")
    print(question)

    print("\n==============================")
    print("ANSWER")
    print("==============================")
    print(answer)