package main

import (
	"encoding/json"
	"fmt"
	"github.com/spf13/cobra"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
)

var noteIdFlag int
var allNotesFlag bool

const rest_api string = "http://localhost:5000"

type Note struct {
	Desc string `json:"desc"`
	ID   int    `json:"id"`
	Name string `json:"name"`
}

type NotesResponse struct {
	Notes []Note `json:"Notes"`
}

type SpecificNote struct {
	Id       int    `json:"id"`
	Note     string `json:"note"`
	NoteName string `json:"note_name"`
}

func main() {
	var rootCmd = &cobra.Command{
		Use:   "client",
		Short: "note and task management cli tool",
		Long:  `note and task management cli tool`,
	}

	var noteCmd = &cobra.Command{
		Use:   "note",
		Short: "note management subcommand",
		Long:  `note management subcommand`,
		Run: func(cmd *cobra.Command, args []string) {
			if len(args) == 0 {
				fmt.Println("Available Commands: ")
				fmt.Println(" get\t get note details")
				fmt.Println(" add\t add new note")
				fmt.Println(" update\t update note")
				fmt.Println(" delete\t delete note")
			}
		},
	}

	var taskCmd = &cobra.Command{
		Use:   "task",
		Short: "task management subcommand",
		Long:  `task management subcommand`,
		Run: func(cmd *cobra.Command, args []string) {
			if len(args) == 0 {
				fmt.Println("Available Commands: ")
				fmt.Println(" get\t get task details")
				fmt.Println(" add\t add new task")
				fmt.Println(" update\t update task")
				fmt.Println(" delete\t delete task")
			}
		},
	}

	noteGetCmd := &cobra.Command{
		Use:   "get",
		Short: "get note details",
		Long:  "get note details",
		Run: func(cmd *cobra.Command, args []string) {
			if allNotesFlag && len(args) == 0 && noteIdFlag == 0 {
				fmt.Println("Getting all notes from remote api endpoint api/v1/notes\n")

				resp, err := http.Get(rest_api + "/api/v1/notes")
				if err != nil {
					panic(err)
				}
				defer resp.Body.Close()

				body, err := ioutil.ReadAll(resp.Body)
				if err != nil {
					log.Fatal("Error reading response body:", err)
				}

				var notesResponse NotesResponse
				err = json.Unmarshal(body, &notesResponse)
				if err != nil {
					log.Fatal("Error marhsalling to struct from json:", err)
				}

				fmt.Println("Id\tName\t\tDescription")
				for _, note := range notesResponse.Notes {
					fmt.Printf("%d\t%s\t\t%s\n", note.ID, note.Name, note.Desc)
				}

				return

			} else if !allNotesFlag && len(args) == 0 && noteIdFlag == 0 {
				fmt.Println("enter --id <id> to get specific note or --all to get all notes")

				return
			} else if allNotesFlag && len(args) > 0 {
				fmt.Println("--all flag should be run without value")
				return
			} else if !allNotesFlag && len(args) == 0 && noteIdFlag != 0 {
				fmt.Printf("getting note id %d from api\n", noteIdFlag)
				resp, err := http.Get(rest_api + "/api/v1/notes/" + strconv.Itoa(noteIdFlag))
				if err != nil {
					panic(err)
				}
				defer resp.Body.Close()

				body, err := ioutil.ReadAll(resp.Body)
				if err != nil {
					log.Fatal("Error reading response body:", err)
				}

				// var note Note
				var note struct{ Note SpecificNote }
				err = json.Unmarshal(body, &note)
				if err != nil {
					log.Fatal("Error marhsalling to struct from json:", err)
				}

				fmt.Println("\nId\tName\t\tDescription")
				fmt.Printf("%d\t%s\t\t%s\n", note.Note.Id,
					note.Note.NoteName, note.Note.Note)

			}

		},
	}

	noteGetCmd.Flags().IntVarP(&noteIdFlag, "id", "i", 0, "get specified note")
	noteGetCmd.Flags().BoolVarP(&allNotesFlag, "all", "a", false, "get all notes")

	noteAddCmd := &cobra.Command{
		Use:   "add",
		Short: "add new note",
		Long:  "get new note",
		Run: func(cmd *cobra.Command, args []string) {
			if len(args) == 0 {
				fmt.Println("enter note --name <name> and --desc <desc> to add")
				return
			}
		},
	}

	noteUpdateCmd := &cobra.Command{
		Use:   "update",
		Short: "update note",
		Long:  "update note",
		Run: func(cmd *cobra.Command, args []string) {
			if len(args) == 0 {
				fmt.Println("enter note --id <id> and --name <name> --desc <desc> to update")
				return
			}
		},
	}

	noteDeleteCmd := &cobra.Command{
		Use:   "delete",
		Short: "delete note",
		Long:  "delete note",
		Run: func(cmd *cobra.Command, args []string) {
			if len(args) == 0 {
				fmt.Println("enter note --id to delete")
				return
			}
		},
	}

	taskGetCmd := &cobra.Command{
		Use:   "get",
		Short: "get task details",
		Long:  "get task details",
		Run: func(cmd *cobra.Command, args []string) {
			if len(args) == 0 {
				fmt.Println("enter --id <id> to get specific note or --all to get all notes")
				return
			}
			fmt.Println(args)
		},
	}

	taskAddCmd := &cobra.Command{
		Use:   "add",
		Short: "add new task",
		Long:  "get new task",
		Run: func(cmd *cobra.Command, args []string) {
			if len(args) == 0 {
				fmt.Println("enter note --name <name> and --desc <desc> to add")
				return
			}
		},
	}

	taskUpdateCmd := &cobra.Command{
		Use:   "update",
		Short: "update task",
		Long:  "update task",
		Run: func(cmd *cobra.Command, args []string) {
			if len(args) == 0 {
				fmt.Println("enter note --id <id> and --name <name> --desc <desc> to update")
				return
			}
		},
	}

	taskDeleteCmd := &cobra.Command{
		Use:   "delete",
		Short: "delete task",
		Long:  "delete task",
		Run: func(cmd *cobra.Command, args []string) {
			if len(args) == 0 {
				fmt.Println("enter note --id to delete")
				return
			}
		},
	}

	rootCmd.CompletionOptions.DisableDefaultCmd = true

	rootCmd.AddCommand(noteCmd)
	rootCmd.AddCommand(taskCmd)

	noteCmd.AddCommand(noteGetCmd)
	noteCmd.AddCommand(noteAddCmd)
	noteCmd.AddCommand(noteUpdateCmd)
	noteCmd.AddCommand(noteDeleteCmd)

	taskCmd.AddCommand(taskGetCmd)
	taskCmd.AddCommand(taskAddCmd)
	taskCmd.AddCommand(taskUpdateCmd)
	taskCmd.AddCommand(taskDeleteCmd)

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
