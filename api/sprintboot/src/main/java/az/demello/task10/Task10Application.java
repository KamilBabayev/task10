package az.demello.task10;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Task10Application {

	public static void main(String[] args) {
		System.out.println("aaaaaaaaaaaaaaaaaaaa");
		System.out.println("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW");
		String demo = System.getenv("VAR1");
		System.out.println("var1: " + demo);
		SpringApplication.run(Task10Application.class, args);
	}
}
