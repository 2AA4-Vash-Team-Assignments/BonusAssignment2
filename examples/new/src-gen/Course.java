import java.util.ArrayList;
import java.util.List;

public class Course {

    private List<Assignment> assignments;
    private Textbook textbook;

    public Course() {
        this.assignments = new ArrayList<>();
    }

    public List<Assignment> getAssignments() {
        return this.assignments;
    }

    public void setAssignments(List<Assignment> assignments) {
        this.assignments = assignments;
    }

    public void addAssignment(Assignment assignment) {
        this.assignments.add(assignment);
    }

    public Textbook getTextbook() {
        return this.textbook;
    }

    public void setTextbook(Textbook textbook) {
        this.textbook = textbook;
    }
}
