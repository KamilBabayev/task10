package az.demello.task10.entity;

import jakarta.annotation.Nullable;
import jakarta.persistence.*;
import org.antlr.v4.runtime.misc.NotNull;


@Entity
@Table(name="notes")
public class Note {

    @Id
//    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(nullable = true)
    private Long Id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String description;

    public Long getId() {
        return Id;
    }

    public void setId(Long id) {
        Id = id;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
