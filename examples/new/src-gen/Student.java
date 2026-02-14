import java.util.ArrayList;
import java.util.List;

public class Student extends Person {

    private List<Course> courses;
    private List<Grade> grades;

    public Student() {
        this.courses = new ArrayList<>();
        this.grades = new ArrayList<>();
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

    public List<Grade> getGrades() {
        return this.grades;
    }

    public void setGrades(List<Grade> grades) {
        this.grades = grades;
    }

    public void addGrade(Grade grade) {
        this.grades.add(grade);
    }
}
