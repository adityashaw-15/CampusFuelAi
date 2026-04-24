package com.spendwise;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Executors;

public class CampusFuelServer {
    private static final int PORT = Integer.parseInt(System.getenv().getOrDefault("PORT", "8080"));
    private static final ObjectMapper JSON = new ObjectMapper();
    private static final HttpClient HTTP = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(10)).build();
    private static final Path STATIC_ROOT = Paths.get(System.getProperty("user.dir")).toAbsolutePath().normalize();

    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);
        CampusFuelServer app = new CampusFuelServer();
        server.createContext("/api/analyze", app::handleAnalyze);
        server.createContext("/", app::handleStaticFile);
        server.setExecutor(Executors.newFixedThreadPool(8));
        server.start();

        System.out.println("CampusFuel AI running at http://localhost:" + PORT);
    }

    private void handleAnalyze(HttpExchange exchange) throws IOException {
        addCorsHeaders(exchange.getResponseHeaders());
        if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
            exchange.sendResponseHeaders(204, -1);
            return;
        }

        try {
            if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                sendJson(exchange, 405, new ErrorResponse("Method not allowed"));
                return;
            }

            AnalyzeRequest req = readJson(exchange, AnalyzeRequest.class);
            AnalyzeResponse res = callGemini(req);
            sendJson(exchange, 200, res);

        } catch (Exception ex) {
            ex.printStackTrace();
            sendJson(exchange, 500, new ErrorResponse("Server error during analysis: " + ex.getMessage()));
        }
    }

    private AnalyzeResponse callGemini(AnalyzeRequest req) {
        String apiKey = "AIzaSyBHJfDNADw4pMr0OzRXweYxdedK_Rnyd8g";

        try {
            String url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + apiKey;
            
            String prompt = """
                    You are CampusFuel AI, a student nutrition and fitness assistant.
                    User Details:
                    - Height: %s cm
                    - Weight: %s kg
                    - Workout Intensity: %s
                    Foods Eaten Today:
                    %s
                    
                    Please analyze this and return ONLY a valid JSON object matching exactly this schema:
                    {
                      "calories": 2100,
                      "protein": 65,
                      "carbs": 250,
                      "junkLevel": 4,
                      "rating": "Good" | "Average" | "Poor",
                      "heartScore": 85,
                      "dailyScore": 7.5,
                      "summary": "Brief student-friendly feedback...",
                      "proteinNote": "Good protein for your workout...",
                      "carbNote": "Energy is balanced...",
                      "junkNote": "Watch the late night snacks...",
                      "suggestions": ["Swap cola for diet cola", "Add 2 eggs to breakfast"],
                      "habits": ["Drink 2L of water", "Eat 1 piece of fruit"],
                      "recipes": ["Microwave Egg Mug: 2 eggs, salt..."]
                    }
                    """.formatted(req.height(), req.weight(), req.workout(), req.foods());

            ObjectNode rootNode = JSON.createObjectNode();
            ArrayNode contentsNode = rootNode.putArray("contents");
            ObjectNode partsNode = JSON.createObjectNode();
            ArrayNode partsArray = JSON.createArrayNode();
            ObjectNode textNode = JSON.createObjectNode();
            textNode.put("text", prompt);
            partsArray.add(textNode);
            partsNode.set("parts", partsArray);
            contentsNode.add(partsNode);

            HttpRequest request = HttpRequest.newBuilder(URI.create(url))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(JSON.writeValueAsString(rootNode)))
                    .build();

            HttpResponse<String> response = HTTP.send(request, HttpResponse.BodyHandlers.ofString());
            System.out.println("GEMINI RESPONSE: " + response.body());
            JsonNode geminiJson = JSON.readTree(response.body());
            
            if (geminiJson.has("candidates") && geminiJson.get("candidates").size() > 0) {
                String textResponse = geminiJson.get("candidates").get(0).path("content").path("parts").get(0).path("text").asText();
                String cleaned = textResponse.replaceAll("```json", "").replaceAll("```", "").trim();
                return JSON.readValue(cleaned, AnalyzeResponse.class);
            }

        } catch (Exception ex) {
            System.err.println("Gemini API failed: " + ex.getMessage());
        }

        return mockResponse();
    }

    private AnalyzeResponse mockResponse() {
        return new AnalyzeResponse(
            2200, 80, 200, 5, "Average", 75, 6.5,
            "Mock Mode: Looks like a decent day! Provide a GEMINI_API_KEY to see real AI analysis.",
            "Try to hit 100g", "Carbs are fine", "A bit high on sugar",
            List.of("Reduce midnight snacks", "Add more veggies"),
            List.of("Drink 2L water", "Stretch for 10 mins"),
            List.of("Healthy Paneer Wrap")
        );
    }

    private void handleStaticFile(HttpExchange exchange) throws IOException {
        if (!"GET".equalsIgnoreCase(exchange.getRequestMethod()) && !"HEAD".equalsIgnoreCase(exchange.getRequestMethod())) {
            sendPlain(exchange, 405, "Method not allowed");
            return;
        }

        String requestPath = exchange.getRequestURI().getPath();
        if ("/".equals(requestPath)) {
            requestPath = "/index.html";
        }

        Path file = STATIC_ROOT.resolve(requestPath.substring(1)).normalize();
        if (!file.startsWith(STATIC_ROOT) || Files.isDirectory(file) || !Files.exists(file)) {
            sendPlain(exchange, 404, "File not found");
            return;
        }

        Headers headers = exchange.getResponseHeaders();
        headers.set("Content-Type", contentType(file));
        headers.set("Cache-Control", "no-store");
        long length = Files.size(file);
        exchange.sendResponseHeaders(200, "HEAD".equalsIgnoreCase(exchange.getRequestMethod()) ? -1 : length);
        if (!"HEAD".equalsIgnoreCase(exchange.getRequestMethod())) {
            try (OutputStream body = exchange.getResponseBody()) {
                Files.copy(file, body);
            }
        }
    }

    private static <T> T readJson(HttpExchange exchange, Class<T> type) throws IOException {
        try (InputStream body = exchange.getRequestBody()) {
            return JSON.readValue(body, type);
        }
    }

    private static void sendJson(HttpExchange exchange, int status, Object payload) throws IOException {
        byte[] bytes = JSON.writeValueAsBytes(payload);
        Headers headers = exchange.getResponseHeaders();
        addCorsHeaders(headers);
        headers.set("Content-Type", "application/json; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream body = exchange.getResponseBody()) {
            body.write(bytes);
        }
    }

    private static void sendPlain(HttpExchange exchange, int status, String message) throws IOException {
        byte[] bytes = message.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "text/plain; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream body = exchange.getResponseBody()) {
            body.write(bytes);
        }
    }

    private static void addCorsHeaders(Headers headers) {
        headers.set("Access-Control-Allow-Origin", "*");
        headers.set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        headers.set("Access-Control-Allow-Headers", "Content-Type");
    }

    private static String contentType(Path file) {
        String name = file.getFileName().toString().toLowerCase();
        if (name.endsWith(".html")) return "text/html; charset=utf-8";
        if (name.endsWith(".css")) return "text/css; charset=utf-8";
        if (name.endsWith(".js")) return "application/javascript; charset=utf-8";
        if (name.endsWith(".png")) return "image/png";
        return "application/octet-stream";
    }

    public record AnalyzeRequest(String foods, String height, String weight, String workout) {}
    public record AnalyzeResponse(
            int calories, int protein, int carbs, int junkLevel,
            String rating, int heartScore, double dailyScore,
            String summary, String proteinNote, String carbNote, String junkNote,
            List<String> suggestions, List<String> habits, List<String> recipes
    ) {}
    public record ErrorResponse(String message) {}
}
