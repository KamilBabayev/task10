package az.demello.task10.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import az.demello.task10.entity.Task;

public interface TaskRepository extends JpaRepository<Task, Long> {
}
