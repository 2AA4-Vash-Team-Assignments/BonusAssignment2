import java.util.ArrayList;
import java.util.List;

public class Professor extends Person {

    private List<Course> courses;

    public Professor() {
        this.courses = new ArrayList<>();
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
