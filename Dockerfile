# Multi-stage build for Spring Boot application
FROM openjdk:17-jdk-slim AS build

# Set working directory
WORKDIR /app

# Copy Maven files
COPY app/pom.xml .
COPY app/.mvn .mvn
COPY app/mvnw .

# Download dependencies
RUN ./mvnw dependency:go-offline -B

# Copy source code
COPY app/src src

# Build the application
RUN ./mvnw clean package -DskipTests

# Runtime stage
FROM openjdk:17-jre-slim

# Create app user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy JAR from build stage
COPY --from=build /app/target/*.jar app.jar

# Change ownership to app user
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/actuator/health || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]