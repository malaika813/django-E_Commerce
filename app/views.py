from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProfileSerializer
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import json

# ✅ Your Gemini API Key
API_KEY = "AIzaSyBPSxsTOEGJctzxL_o8YkYNynwLnwIx3nE"

# ✅ Fixed Gemini model name
MODEL_NAME = "models/gemini-2.5-flash"


@api_view(["GET", "POST"])
def career_recommendation(request):
    """
    Generate AI-based career recommendations using Gemini API.
    """
    if request.method == "POST":
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            degree = data["degree"]
            skills = data["skills"]
            interests = data["interests"]

            # --- Build prompt ---
            prompt = f"""
            I am a fresh graduate with a degree in {degree}.
            My skills include {skills}.
            My interests are {interests}.
            Suggest 3 suitable career paths for me with brief reasoning and a learning roadmap.
            """

            # --- Gemini API endpoint ---
            url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}

            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                result = response.json()

                # --- Extract text safely ---
                text = (
                    result.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text", "No response from model.")
                )

                return Response({"recommendations": text})

            except Exception as e:
                return Response({"error": str(e)}, status=500)

        return Response(serializer.errors, status=400)

    # For GET requests (show form page)
    return render(request, "profile_form.html")






def chat_page(request):
    """Render the chatbot UI page."""
    return render(request, "chatbot.html")


@csrf_exempt
def chat_api(request):
    """Handle real-time chat messages using Gemini API."""
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        user_message = data.get("message", "")

        if not user_message:
            return JsonResponse({"reply": "Please type something!"})

        # --- Gemini API request ---
        url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:generateContent?key={API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": user_message}]}]
        }

        try:
            response = requests.post(url, json=payload)
            result = response.json()

            reply = (
                result.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "⚠️ No reply from AI.")
            )

            return JsonResponse({"reply": reply})

        except Exception as e:
            return JsonResponse({"reply": f"Error: {str(e)}"})

    return JsonResponse({"reply": "Invalid request method."})