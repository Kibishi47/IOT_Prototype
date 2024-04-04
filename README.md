# IOT_Prototype

## Sequence diagram for initialisation of ESP32
```mermaid
sequenceDiagram
    actor User
    participant Display
    participant ESP32
    participant Initialisation
    participant Button
    participant Accelerometer
    participant UltrasonicSensor
    participant WebSocketServer
    participant Tests

    User->>ESP32: Start ESP

    %% INITIALISATION
    ESP32->>Initialisation: Start Initialisation
    Initialisation->>Button: Initialize button
    Initialisation->>Accelerometer: Initialize accelerometer
    Initialisation->>UltrasonicSensor: Initialize ultrasonic sensor
    Initialisation->>WebSocketServer: Start server

    %% TESTS
    ESP32->>Tests: Starting tests
    User->>Button: Test button
    Button-->>Tests: Test result
    alt Is detected
        Tests->>Display: Show good fonctionnement
        Display-->>User: See good fonctionnement

        ESP32->>Accelerometer: Test accelerometer
        Accelerometer-->>Tests: Test result
        alt Accelerometer is correct
            Tests->>Display: Show good fonctionnement
            Display-->>User: See good fonctionnement

            ESP32->>UltrasonicSensor: Test ultrasonic sensor
            UltrasonicSensor-->>Tests: Test result
            alt UltrasonicSensor is correct
                Tests->>Display: Show good fonctionnement
                Display-->>User: See good fonctionnement

                ESP32->>WebSocketServer: Check server is launched
                WebSocketServer-->>Tests: Check result
                alt Server is launched
                    Tests->>Display: Show good fonctionnement
                    Display-->>User: See good fonctionnement
                else
                    Tests->>Display: Show bad fonctionnement
                    Display-->>User: See bad fonctionnement
                    Tests->>ESP32: Stop Tests
                end
            else
                Tests->>Display: Show bad fonctionnement
                Display-->>User: See bad fonctionnement
                Tests->>ESP32: Stop Tests
            end
        else
            Tests->>Display: Show bad fonctionnement
            Display-->>User: See bad fonctionnement
            Tests->>ESP32: Stop Tests
        end
    else
        Tests->>Display: Show bad fonctionnement
        Display-->>User: See bad fonctionnement
        Tests->>ESP32: Stop Tests
    end
```

## Flow diagram for run of ESP32
```mermaid
graph TD
    A[Start] --> B(Initialize Components)
    B --> C{While True Loop}
    C --> |Button Clicked| D[Detect Button State Change]
    D --> E{State Change?}
    E --> |Yes| F[Send Button State via Socket]
    F --> C
    E --> |No| G{Button Not Clicked for 10 min?}
    G --> |Yes| H[Launch Error Code]
    G --> |No| C
    C --> |Accelerometer Movement| I[Detect Accelerometer Movement]
    I --> J{Movement Detected?}
    J --> |Yes| K[Send Movement via Socket]
    K --> C
    J --> |No| L{No Movement for 3 seconds?}
    L --> |Yes| M[Launch Error Code]
    L --> |No| C
    C --> |Ultrasonic Sensor Distance| N[Detect Ultrasonic Sensor Distance]
    N --> O{Distance Conformity?}
    O --> |Yes| P[Send Conformity Status via Socket]
    P --> C
    O --> |No| Q{No Distance Detected for 3 seconds?}
    Q --> |Yes| R[Launch Error Code]
    Q --> |No| C
    C --> |WebSocket Status| S[Check WebSocket Status]
    S --> T{Server Online?}
    T --> |Yes| U{New Clients?}
    U --> |Yes| V[Handle New Clients]
    V --> C
    U --> |No| W{Clients Disconnected?}
    W --> |Yes| X[Handle Disconnections]
    X --> C
    W --> |No| C
    T --> |No| Y[Launch Error Code]
````

