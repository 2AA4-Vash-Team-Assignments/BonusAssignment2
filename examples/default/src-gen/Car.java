import java.util.ArrayList;
import java.util.List;

public class Car {

    private List<Wheel> wheels;
    private LicencePlate licencePlate;

    public Car() {
        this.wheels = new ArrayList<>();
    }

    public List<Wheel> getWheels() {
        return this.wheels;
    }

    public void setWheels(List<Wheel> wheels) {
        this.wheels = wheels;
    }

    public void addWheel(Wheel wheel) {
        this.wheels.add(wheel);
    }

    public LicencePlate getLicencePlate() {
        return this.licencePlate;
    }

    public void setLicencePlate(LicencePlate licencePlate) {
        this.licencePlate = licencePlate;
    }
}
