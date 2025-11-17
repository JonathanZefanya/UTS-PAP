import java.util.*;

// Enum untuk status pesanan
enum OrderStatus {
    CREATE(0),
    SHIPPING(1),
    DELIVERED(2),
    PAID(3);

    private int value;

    OrderStatus(int value) {
        this.value = value;
    }

    public int getValue() {
        return value;
    }
}

// =====================================
// Entity Classes
// =====================================

class Customer {
    private String name;
    private String deliveryAddress;
    private String contact;
    private boolean active;
    private List<Order> orders = new ArrayList<>();

    public Customer(String name, String address, String contact, boolean active) {
        this.name = name;
        this.deliveryAddress = address;
        this.contact = contact;
        this.active = active;
    }

    public void addOrder(Order order) {
        orders.add(order);
    }

    public List<Order> getOrders() {
        return orders;
    }
}

class Item {
    private float weight;
    private String description;

    public Item(String description, float weight) {
        this.description = description;
        this.weight = weight;
    }

    public float getPriceForQuantity(int qty) {
        // Dummy implementation
        return qty * 10.0f;
    }

    public float getWeight() {
        return weight;
    }
}

class Order {
    private Date createDate;
    private OrderStatus status;
    private Customer customer;
    private List<OrderDetail> orderDetails = new ArrayList<>();
    private List<Payment> payments = new ArrayList<>();

    public Order(Customer customer, Date date) {
        this.customer = customer;
        this.createDate = date;
        this.status = OrderStatus.CREATE;
    }

    public void addOrderDetail(OrderDetail detail) {
        orderDetails.add(detail);
    }

    public void addPayment(Payment payment) {
        payments.add(payment);
    }

    public List<OrderDetail> getOrderDetails() {
        return orderDetails;
    }

    public List<Payment> getPayments() {
        return payments;
    }
}

class OrderDetail {
    private int qty;
    private String taxStatus;
    private Item item;

    public OrderDetail(Item item, int qty, String taxStatus) {
        this.item = item;
        this.qty = qty;
        this.taxStatus = taxStatus;
    }

    public float calculateSubTotal() {
        return item.getPriceForQuantity(qty);
    }

    public float calculateWeight() {
        return item.getWeight() * qty;
    }
}

abstract class Payment {
    protected float amount;

    public Payment(float amount) {
        this.amount = amount;
    }

    public float getAmount() {
        return amount;
    }
}

class Credit extends Payment {
    private String number;
    private String type;
    private Date expireDate;

    public Credit(float amount, String number, String type, Date expireDate) {
        super(amount);
        this.number = number;
        this.type = type;
        this.expireDate = expireDate;
    }
}

class Cash extends Payment {
    private float cashTendered;

    public Cash(float amount, float cashTendered) {
        super(amount);
        this.cashTendered = cashTendered;
    }
}

class Check extends Payment {
    private String name;
    private String bankID;

    public Check(float amount, String name, String bankID) {
        super(amount);
        this.name = name;
        this.bankID = bankID;
    }

    public boolean authorized() {
        // Dummy implementation
        return true;
    }
}

class WireTransfer extends Payment {
    private String bankID;
    private String bankName;

    public WireTransfer(float amount, String bankID, String bankName) {
        super(amount);
        this.bankID = bankID;
        this.bankName = bankName;
    }
}