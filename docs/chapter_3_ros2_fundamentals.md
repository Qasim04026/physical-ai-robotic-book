# Chapter 3: ROS2 Fundamentals

The Robot Operating System (ROS) has become the de facto standard framework for robot software development. ROS2, the next generation of ROS, addresses many limitations of its predecessor, offering improved real-time capabilities, enhanced security, and better support for multi-robot systems and diverse hardware. This chapter introduces the fundamental concepts of ROS2, guiding you through its architecture, core components, and basic usage, which are essential for building sophisticated physical AI and humanoid robotics applications.

## What is ROS2?

ROS2 is an open-source, meta-operating system for robots. It provides a flexible framework for writing robot software, offering a collection of tools, libraries, and conventions that simplify the complex task of building robotic applications. Key characteristics of ROS2 include:

*   **Distributed Architecture:** ROS2 is designed for distributed computing, allowing different parts of a robot system (e.g., sensor drivers, navigation algorithms, motor controllers) to run as independent processes (nodes) on potentially different machines.
*   **Inter-process Communication:** It provides robust mechanisms for nodes to communicate with each other through topics, services, and actions, enabling modular and decoupled software design.
*   **Middleware Agnostic:** Unlike ROS1 which was tied to its own communication system, ROS2 uses industry-standard Data Distribution Service (DDS) as its primary middleware, offering flexibility and better performance. It can also support other middlewares.
*   **Real-time Capabilities:** ROS2 is designed with real-time performance in mind, crucial for critical robot control systems.
*   **Security:** It includes security features for authentication, encryption, and access control, important for deployed robotic systems.
*   **Language Support:** Supports C++ and Python (and potentially other languages) with client libraries.

## ROS2 Concepts

Understanding these core concepts is crucial for working with ROS2:

1.  **Nodes:** A node is an executable process that performs a computation. Typically, a robot control system is composed of many nodes, each responsible for a specific task (e.g., a camera driver node, a motor control node, a localization node).
2.  **Topics:** Topics are a primary mechanism for nodes to exchange data asynchronously. A node can publish messages to a topic, and other nodes can subscribe to that topic to receive the messages. This is a one-to-many communication model.
    ```cpp
    // Example: ROS2 C++ Publisher Node (conceptual)
    #include "rclcpp/rclcpp.hpp"
    #include "std_msgs/msg/string.hpp"

    class SimplePublisher : public rclcpp::Node
    {
    public:
        SimplePublisher() : Node("simple_publisher"), count_(0)
        {
            publisher_ = this->create_publisher<std_msgs::msg::String>("chatter", 10);
            timer_ = this->create_wall_timer(
                std::chrono::seconds(1),
                std::bind(&SimplePublisher::timer_callback, this));
        }

    private:
        void timer_callback()
        {
            auto message = std_msgs::msg::String();
            message.data = "Hello, world! " + std::to_string(count_++);
            RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
            publisher_->publish(message);
        }
        rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
        rclcpp::TimerBase::SharedPtr timer_;
        size_t count_;
    };

    int main(int argc, char * argv[])
    {
        rclcpp::init(argc, argv);
        rclcpp::spin(std::make_shared<SimplePublisher>());
        rclcpp::shutdown();
        return 0;
    }
    ```
    ```python
    # Example: ROS2 Python Subscriber Node (conceptual)
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String

    class SimpleSubscriber(Node):
        def __init__(self):
            super().__init__('simple_subscriber')
            self.subscription = self.create_subscription(
                String, 'chatter', self.listener_callback, 10)
            self.subscription # prevent unused variable warning

        def listener_callback(self, msg):
            self.get_logger().info('I heard: "%s"' % msg.data)

    def main(args=None):
        rclpy.init(args=args)
        simple_subscriber = SimpleSubscriber()
        rclpy.spin(simple_subscriber)
        simple_subscriber.destroy_node()
        rclpy.shutdown()

    if __name__ == '__main__':
        main()
    ```
3.  **Services:** Services enable synchronous, request/response communication between nodes. A client node sends a request to a service server node and waits for a response. This is a one-to-one communication model, often used for discrete, immediate actions.
4.  **Actions:** Actions are designed for long-running tasks where feedback and preemption are required. An action client sends a goal to an action server, receives continuous feedback on the goal's progress, and can cancel the goal if needed. This is commonly used for navigation tasks (e.g., "go to X, Y") or complex manipulation.
5.  **Messages:** Messages are data structures used for communication over topics, services, and actions. ROS2 provides a rich set of standard message types (e.g., `std_msgs/msg/String`, `sensor_msgs/msg/Image`, `geometry_msgs/msg/Twist`) and allows users to define custom message types.
6.  **Parameters:** Parameters allow nodes to expose configurable values at runtime. They can be set dynamically and provide a way to tune node behavior without recompiling.
7.  **Launch Files:** Launch files are XML or Python scripts used to start multiple ROS2 nodes with their associated parameters and configurations. They simplify the process of deploying a complex robot system.
8.  **Packages:** ROS2 software is organized into packages. A package is a collection of nodes, libraries, configuration files, message definitions, and other resources. Packages are the fundamental unit of ROS2 development.

## ROS2 Workspace and Build System (Colcon)

Developing with ROS2 typically involves a workspace, which is a directory that contains a set of ROS2 packages. `colcon` is the build tool used in ROS2.

### Creating a Workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

### Building Packages

After placing your packages in the `src` directory, you can build them:

```bash
cd ~/ros2_ws
colcon build
```

### Sourcing the Environment

Before running any ROS2 commands or nodes, you must source the ROS2 environment setup files and your workspace setup files:

```bash
source /opt/ros/humble/setup.bash # Replace humble with your ROS2 distribution
source ~/ros2_ws/install/setup.bash
```

It's common to add these `source` commands to your `~/.bashrc` or `~/.zshrc` file for convenience.

## Basic ROS2 Command Line Tools

ROS2 provides a suite of command-line tools for introspection, debugging, and interaction with a running system:

*   `ros2 run <package_name> <executable_name>`: Runs a ROS2 node.
*   `ros2 topic list`: Lists all active topics.
*   `ros2 topic echo <topic_name>`: Displays messages being published on a topic.
*   `ros2 topic pub <topic_name> <message_type> <args>`: Publishes a single message to a topic.
*   `ros2 node list`: Lists all active nodes.
*   `ros2 service list`: Lists all available services.
*   `ros2 service call <service_name> <service_type> <args>`: Calls a service.
*   `ros2 param list`: Lists parameters for a node.
*   `ros2 launch <package_name> <launch_file_name>`: Launches multiple nodes from a launch file.

## Conclusion

ROS2 provides a powerful and flexible framework for developing complex robotic applications. By understanding its fundamental concepts – nodes, topics, services, actions, messages, and the `colcon` build system – you gain the essential tools to design, implement, and deploy sophisticated physical AI and humanoid robotics systems. The modular and distributed nature of ROS2 allows for collaborative development and efficient integration of various robotic components, making it an indispensable skill for modern robotics engineers. The next chapter will delve into more advanced ROS2 features and best practices.