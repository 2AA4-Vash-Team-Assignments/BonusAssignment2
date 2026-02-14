import java.util.ArrayList;
import java.util.List;

public class Department {

    private List<Professor> professors;
    private List<Course> courses;

    public Department() {
        this.professors = new ArrayList<>();
        this.courses = new ArrayList<>();
    }

    public List<Professor> getProfessors() {
        return this.professors;
    }

    public void setProfessors(List<Professor> professors) {
        this.professors = professors;
    }

    public void addProfessor(Professor professor) {
        this.professors.add(professor);
    }

    public List<Course> getCourses() {
        return this.courses;
    }

    public void setCourses(List<Course> courses) {
        this.courses = courses;
    }

    public void addCourse(Course course) {
        this.courses.add(course);
    }
}
