package az.demello.task10.controller;

import az.demello.task10.repository.NoteRepository;
import az.demello.task10.service.NoteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import az.demello.task10.entity.Note;

import java.util.List;

@RestController
@RequestMapping("/api/v1")
public class NoteController {

    @Autowired
    private NoteService noteService;

    @GetMapping("/notes")
    private List<Note> getAllNotes() {
        return noteService.getAllNotes();
    }

    @PostMapping("/notes")
    private Note createNote(@RequestBody Note note) {
        System.out.println(note);
        System.out.println("id: " + note.getId());
        System.out.println("name: " + note.getName());
        System.out.println("description: " + note.getDescription());
        return noteService.saveNote(note);
    }
}
