package az.demello.task10.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name="tasks")
public class Task {
    @Id
    private Long Id;

    @Column
    private String name;

    @Column(nullable = false)
    private String description;

    @Column
    private String status;

    @Column(name="created_at", nullable = false)
    private LocalDateTime createdAt;

    public Long getId() {
        return Id;
    }

    public void setId(Long id) {
        Id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDesc() {
        return description;
    }

    public void setDesc(String desc) {
        this.description = description;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
