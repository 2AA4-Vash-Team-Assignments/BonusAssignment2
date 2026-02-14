import java.util.ArrayList;
import java.util.List;

public class University {

    private List<Department> departments;
    private List<Building> buildings;

    public University() {
        this.departments = new ArrayList<>();
        this.buildings = new ArrayList<>();
    }

    public List<Department> getDepartments() {
        return this.departments;
    }

    public void setDepartments(List<Department> departments) {
        this.departments = departments;
    }

    public void addDepartment(Department department) {
        this.departments.add(department);
    }

    public List<Building> getBuildings() {
        return this.buildings;
    }

    public void setBuildings(List<Building> buildings) {
        this.buildings = buildings;
    }

    public void addBuilding(Building building) {
        this.buildings.add(building);
    }
}
