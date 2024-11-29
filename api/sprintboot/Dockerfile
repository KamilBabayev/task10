FROM gradle:8.3-jdk17 as builder

WORKDIR /app

COPY build.gradle build.gradle

COPY gradlew gradlew

COPY gradle gradle

COPY settings.gradle settings.gradle

COPY src src

RUN chmod +x gradlew

RUN ./gradlew build

FROM openjdk:17-jdk-slim

WORKDIR /app

COPY --from=builder /app/build/libs/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/app/app.jar"]