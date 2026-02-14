import java.util.ArrayList;
import java.util.List;

public class Building {

    private List<Room> rooms;

    public Building() {
        this.rooms = new ArrayList<>();
    }

    public List<Room> getRooms() {
        return this.rooms;
    }

    public void setRooms(List<Room> rooms) {
        this.rooms = rooms;
    }

    public void addRoom(Room room) {
        this.rooms.add(room);
    }
}
