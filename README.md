# CampusFuel AI - Smart Nutrition Assistant

**CampusFuel AI** is a smart, dynamic student nutrition and fitness assistant built for the **Google Antigravity Hackathon**.

## Chosen Vertical
**Health & Fitness (Student Nutrition Assistant)**

## Approach and Logic
CampusFuel AI bridges the gap between complicated macro-tracking apps and the reality of student life (eating mess food, instant noodles, and cafeteria snacks). Instead of relying on a rigid local database, it uses **Google Gemini AI** to act as a dynamic nutrition coach.

### How it works:
1. **User Profile:** Enter your Height, Weight, and Workout Intensity. The app instantly calculates your BMI.
2. **Food Logging:** Type your daily food intake in natural language (e.g., "2 eggs, a burger, and a cola").
3. **AI Evaluation (Gemini Integration):** The frontend sends your profile and food log to the Java backend (`/api/analyze`). The backend securely communicates with the **Gemini API** via a structured prompt to generate a JSON response containing:
   - Estimated Calories, Protein, and Carbs.
   - A realistic "Junk Level" and "Heart Health Score" out of 100 based on your workout intensity and food choices.
   - Actionable "Habits" to start.
   - Dynamic, healthy "Recipes" tailored for students.

### Assumptions Made
- We assume students prefer qualitative, "vibe-check" style feedback rather than exact gram-for-gram counting.
- The BMI calculation uses standard metric formulas.
- The app assumes the user will supply a valid `GEMINI_API_KEY` in their environment variables to unleash the full power of the AI.

## Getting Started
1. Set your `GEMINI_API_KEY` as an environment variable.
2. Compile and run the Java backend: `CampusFuelServer.java`.
3. Open `http://localhost:8080` in your browser.
