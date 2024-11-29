package az.demello.task10.controller;

import az.demello.task10.service.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import az.demello.task10.entity.Task;

import java.util.List;

@RestController
@RequestMapping("/api/v1")
public class TaskController {
    @Autowired
    private TaskService taskService;

    @GetMapping("/tasks")
    public List<Task> getTasks() {
        return taskService.getAllTasks();
    }

    @PostMapping("/tasks")
    public Task createTask(@RequestBody Task task) {
        return taskService.saveTask(task);
    }
}
