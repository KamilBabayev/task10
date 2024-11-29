package az.demello.task10.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import az.demello.task10.entity.Note;

public interface NoteRepository extends JpaRepository<Note, Long> {
}
