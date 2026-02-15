from django.db.models import Q
from schemes.models import Scheme
from chatbot.services.gemini_service import generate_ai_response


def recommend_schemes(user, message):
    """
    Hybrid Recommendation System:
    1. Intelligent DB filtering
    2. Gemini explanation layer
    """

    # Start with active schemes only
    queryset = Scheme.objects.filter(is_active=True)

    # -------------------------
    # FILTERING LOGIC
    # -------------------------

    # Income Filter
    if user.income is not None:
        queryset = queryset.filter(
            Q(income_limit__isnull=True) |
            Q(income_limit__gte=user.income)
        )

    # Residence Type Filter
    if user.residence_type:
        queryset = queryset.filter(
            Q(residence_type__isnull=True) |
            Q(residence_type=user.residence_type)
        )

    # Category Filter (SC/ST/OBC/General)
    if user.category:
        queryset = queryset.filter(
            Q(eligible_categories__isnull=True) |
            Q(eligible_categories=user.category)
        )

    # Age Filter
    if user.age is not None:
        queryset = queryset.filter(
            Q(min_age__isnull=True) | Q(min_age__lte=user.age),
            Q(max_age__isnull=True) | Q(max_age__gte=user.age)
        )

    # State Filter
    if user.location:
        queryset = queryset.filter(
            Q(state__isnull=True) |
            Q(state__iexact=user.location)
        )

    # Limit results
    schemes = queryset[:5]

    # -------------------------
    # HANDLE NO MATCH CASE
    # -------------------------

    if not schemes:
        return (
            "I couldn't find exact schemes matching your profile.\n"
            "You can explore more schemes at:\n"
            "• https://www.myscheme.gov.in\n"
            "• https://www.india.gov.in"
        )

    # -------------------------
    # PREPARE SCHEME TEXT
    # -------------------------

    scheme_text = "\n\n".join([
        f"""
Scheme Name: {s.title}
Category: {s.category}
Description: {s.description}
Official Link: {s.official_link}
"""
        for s in schemes
    ])

    # -------------------------
    # GEMINI PROMPT (STEP 2 ADDED)
    # -------------------------

    prompt = f"""
You are an expert AI assistant helping Indian citizens find suitable government schemes.

IMPORTANT RULES:
- Use simple and clear language.
- Clearly explain eligibility.
- Mention official links.
- Do NOT invent schemes.
- Only use the schemes provided below.
- Always respond in the SAME language the user used.
  (If user writes in Hindi → reply in Hindi.
   If English → reply in English.
   If Hinglish → reply naturally.)

User Profile:
Name: {user.name}
Location: {user.location}
Income: {user.income}
Residence Type: {user.residence_type}
Category: {user.category}
Age: {user.age}
Occupation: {user.job_field}

User Question:
{message}

Available Schemes:
{scheme_text}

Now explain which schemes are best for the user and why.
If multiple schemes apply, explain briefly for each.
Keep response structured and easy to read.
"""

    # -------------------------
    # GENERATE RESPONSE
    # -------------------------

    return generate_ai_response(prompt)
