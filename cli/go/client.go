package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/spf13/cobra"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"text/tabwriter"
)

var noteIdFlag int
var noteIdStrFlag string
var allNotesFlag bool
var noteNameFlag string
var noteDescFlag string

var (
	taskIdFlag    int
	taskIdStrFlag string
	allTasksFlag  bool
	taskNameFlag  string
	taskDescFlag  string
)

const rest_api string = "http://localhost:5000"

type Note struct {
	Desc string `json:"desc"`
	ID   int    `json:"id"`
	Name string `json:"name"`
}

type Task struct {
	Desc       string `json:"desc"`
	Id         int    `json:"id"`
	Name       string `json:"name"`
	Status     string `json: "status`
	Created_at string `json: "created_at"`
}

type NotesResponse struct {
	Notes []Note `json:"Notes"`
}

type TasksResponse struct {
	Tasks []Task `json:"Tasks"`
}

type SpecificNote struct {
	Id       int    `json:"id"`
	Note     string `json:"note"`
	NoteName string `json:"note_name"`
}

type specificTask struct {
	CreatedAt string `json:"created_at"`
	Id        int    `json:"id"`
	Status    string `json:"status"`
	Task      string `json:"task"`
	TaskName  string `json:"task_name"`
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
			w := tabwriter.NewWriter(os.Stdout, 0, 0, 1, ' ', tabwriter.TabIndent)

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

				fmt.Fprintln(w, "ID\tName\tDescription")

				for _, note := range notesResponse.Notes {
					fmt.Fprintf(w, "%d\t%s\t%s\n", note.ID, note.Name, note.Desc)
				}
				w.Flush()

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

				var note struct{ Note SpecificNote }

				err = json.Unmarshal(body, &note)
				if err != nil {
					log.Fatal("Error marhsalling to struct from json:", err)
				}

				fmt.Println("\nId\tName\t\tDescription")

				fmt.Printf("%d\t%s\t\t%s\n", note.Note.Id,
					note.Note.NoteName, note.Note.Note)
				w.Flush()

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
			fmt.Println("")

			if len(args) == 0 && len(noteNameFlag) == 0 && len(noteDescFlag) == 0 {
				fmt.Println("enter note --name <name> and --desc <desc> to add")
				return
			} else if len(noteNameFlag) > 0 && len(noteDescFlag) > 0 {

				note := map[string]string{
					"name": noteNameFlag,
					"desc": noteDescFlag,
				}

				jsonData, err := json.Marshal(note)
				if err != nil {
					fmt.Println("Error:", err)
					return
				}

				resp, err := http.Post(rest_api+"/api/v1/notes", "application/json",
					bytes.NewBuffer(jsonData))
				if err != nil {
					fmt.Println("Error:", err)
					return
				}
				defer resp.Body.Close()

				var ResponseBody map[string]interface{}
				if err := json.NewDecoder(resp.Body).Decode(&ResponseBody); err != nil {
					fmt.Println("Error:", err)
					return
				}

				fmt.Println("msg:", ResponseBody["msg"])

			} else if (len(noteNameFlag) > 0 || len(noteDescFlag) == 0) ||
				(len(noteNameFlag) == 0 || len(noteDescFlag) > 0) {
				fmt.Println("enter both --name <name> and --desc <desc>")
				return
			}
		},
	}
	noteAddCmd.Flags().StringVarP(&noteNameFlag, "name", "n", "", "new note name")
	noteAddCmd.Flags().StringVarP(&noteDescFlag, "desc", "d", "", "new note description")

	noteUpdateCmd := &cobra.Command{
		Use:   "update",
		Short: "update note",
		Long:  "update note",
		Run: func(cmd *cobra.Command, args []string) {
			if noteIdFlag == 0 || len(noteNameFlag) == 0 || len(noteDescFlag) == 0 {
				fmt.Println("enter note --id <id> and --name <name> --desc <desc> to update")
				return
			} else if noteIdFlag != 0 && len(noteNameFlag) != 0 && len(noteDescFlag) != 0 {
				fmt.Println("create struct as json")
				note := map[string]string{
					"id":   noteIdStrFlag,
					"name": noteNameFlag,
					"desc": noteDescFlag,
				}

				jsonData, err := json.Marshal(note)
				if err != nil {
					fmt.Println("Error", err)
					return
				}

				req, err := http.NewRequest("PUT", rest_api+"/api/v1/notes/"+strconv.Itoa(noteIdFlag), bytes.NewBuffer(jsonData))
				if err != nil {
					fmt.Println("error", err)
					return
				}

				req.Header.Set("Content-Type", "application/json")
				client := &http.Client{}

				resp, err := client.Do(req)
				if err != nil {
					fmt.Println("welcome", err)
					return
				}
				defer resp.Body.Close()

				body, err := ioutil.ReadAll(resp.Body)
				if err != nil {
					fmt.Println("error reading", err)
					return
				}

				fmt.Println(resp.Status)
				fmt.Println(string(body))
			}
		},
	}
	noteUpdateCmd.Flags().IntVarP(&noteIdFlag, "id", "i", 0, "specify note id to update")
	noteUpdateCmd.Flags().StringVarP(&noteNameFlag, "name", "n", "", "updated note name")
	noteUpdateCmd.Flags().StringVarP(&noteDescFlag, "desc", "d", "", "updated note desc")

	noteDeleteCmd := &cobra.Command{
		Use:   "delete",
		Short: "delete note",
		Long:  "delete note",
		Run: func(cmd *cobra.Command, args []string) {
			if len(args) == 0 && noteIdFlag == 0 {
				fmt.Println("enter note id --id <note_id> to delete")
				return
			} else if len(args) == 0 && noteIdFlag != 0 {
				client := &http.Client{}

				req, err := http.NewRequest("DELETE", rest_api+"/api/v1/notes/"+
					strconv.Itoa(noteIdFlag), nil)
				if err != nil {
					fmt.Println("Error sending request", err)
					return
				}

				resp, err := client.Do(req)
				if err != nil {
					fmt.Println("Error sending request", err)
					return
				}
				defer resp.Body.Close()

				body, err := ioutil.ReadAll(resp.Body)
				if err != nil {
					fmt.Println("Error reading response: ", err)
					return
				}

				fmt.Println(string(body))
			}

		},
	}
	noteDeleteCmd.Flags().IntVarP(&noteIdFlag, "id", "i", 0, "specify note id to delete")

	taskGetCmd := &cobra.Command{
		Use:   "get",
		Short: "get task details",
		Long:  "get task details",
		Run: func(cmd *cobra.Command, args []string) {
			t := tabwriter.NewWriter(os.Stdout, 0, 0, 1, ' ', tabwriter.TabIndent)

			if allTasksFlag && len(args) == 0 && taskIdFlag == 0 {
				fmt.Println("Getting all tasks from remote api endpoint api/v1/tasks\n")
				resp, err := http.Get(rest_api + "/api/v1/tasks")
				if err != nil {
					fmt.Println("error in connection:", err)
					return
				}
				defer resp.Body.Close()

				body, err := ioutil.ReadAll(resp.Body)
				if err != nil {
					fmt.Println("Error reading response body", err)
				}

				var tasksResponse TasksResponse
				err = json.Unmarshal(body, &tasksResponse)
				if err != nil {
					log.Fatal("Error marshalling from json to strcut: ", err)
				}

				fmt.Fprintln(t, "ID\tName\tStatus\tCreated_at\tDescription")

				for _, task := range tasksResponse.Tasks {
					fmt.Fprintf(t, "%d\t%s\t%s\t%s\t%s\n", task.Id, task.Name, task.Status,
						task.Created_at, task.Desc)

				}
				t.Flush()

				return
			} else if allTasksFlag && len(args) > 0 {
				fmt.Println("--all flag should be run without value")
				return
			} else if !allTasksFlag && len(args) == 0 && taskIdFlag == 0 {
				fmt.Println("enter --id <id> to get specific task or --all to get all tasks")

				return
			} else if !allTasksFlag && len(args) == 0 && taskIdFlag != 0 {
				fmt.Printf("getting task id %d from api\n\n", taskIdFlag)

				resp, err := http.Get(rest_api + "/api/v1/tasks/" + strconv.Itoa(taskIdFlag))
				if err != nil {
					panic(err)
				}
				defer resp.Body.Close()

				body, err := ioutil.ReadAll(resp.Body)
				if err != nil {
					fmt.Println("Eror reading response body", err)
				}

				type TaskWrapper struct {
					Task specificTask `json: "task"`
				}

				var taskWrapper TaskWrapper
				if err := json.Unmarshal([]byte(body), &taskWrapper); err != nil {
					fmt.Println("Error:", err)
					return
				}
				// err = json.Unmarshal(body, &task)
				// fmt.Println(err)

				fmt.Printf("Task CreatedAt: %s\n", taskWrapper.Task.CreatedAt)
				fmt.Printf("Task Id: %d\n", taskWrapper.Task.Id)
				fmt.Printf("Task Status: %s\n", taskWrapper.Task.Status)
				fmt.Printf("Task Name: %s\n", taskWrapper.Task.TaskName)
				fmt.Printf("Task Task: %s\n", taskWrapper.Task.Task)
				return
			}
		},
	}
	taskGetCmd.Flags().IntVarP(&taskIdFlag, "id", "i", 0, "get specified task")
	taskGetCmd.Flags().BoolVarP(&allTasksFlag, "all", "a", false, "get all tasks")

	taskAddCmd := &cobra.Command{
		Use:   "add",
		Short: "add new task",
		Long:  "get new task",
		Run: func(cmd *cobra.Command, args []string) {
			if len(args) == 0 && len(taskNameFlag) == 0 && len(taskDescFlag) == 0 {
				fmt.Println("enter task --name <name> and --desc <desc> to add")
				return
			} else if len(taskNameFlag) > 0 && len(taskDescFlag) > 0 {
				task := map[string]string{
					"name": taskNameFlag,
					"desc": taskDescFlag,
				}

				jsonData, err := json.Marshal(task)
				if err != nil {
					fmt.Println("Error while marshaling to json", err)
					return
				}

				resp, err := http.Post(rest_api+"/api/v1/tasks", "application/json",
					bytes.NewBuffer(jsonData))
				if err != nil {
					fmt.Println("Error while posting task data", err)
					return
				}

				defer resp.Body.Close()

				var ResponseBody map[string]interface{}
				if err := json.NewDecoder(resp.Body).Decode(&ResponseBody); err != nil {
					fmt.Println("Error:", err)
					return
				}

				fmt.Println("msg:", ResponseBody["msg"])
			}
		},
	}
	taskAddCmd.Flags().StringVarP(&taskNameFlag, "name", "n", "", "new task name")
	taskAddCmd.Flags().StringVarP(&taskDescFlag, "desc", "d", "", "new task description")

	taskUpdateCmd := &cobra.Command{
		Use:   "update",
		Short: "update task",
		Long:  "update task",
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Println("")

			if len(args) == 0 && len(taskNameFlag) == 0 && len(taskDescFlag) == 0 {
				fmt.Println("enter task --name <name> and --desc <desc> to add")
				return
			}

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
