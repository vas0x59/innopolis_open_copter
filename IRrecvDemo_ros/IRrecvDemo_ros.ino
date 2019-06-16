#include <IRremote.h>
//#include <IRremoteESP8266.h>
//#include <IRrecv.h>
//#include <IRutils.h>
#include <ros.h>
#include <std_msgs/String.h>
int RECV_PIN = 3;
int POWER_PIN = 2;

ros::NodeHandle nh;

std_msgs::String str_msg;
ros::Publisher chatter("ir_reciv", &str_msg);

IRrecv irrecv(RECV_PIN);

decode_results results;

void setup()
{

    pinMode(POWER_PIN, OUTPUT);
    digitalWrite(POWER_PIN, HIGH);
    irrecv.enableIRIn(); // Start the receiver
    nh.initNode();
    nh.advertise(chatter);

}
int i_count = 0;
bool qwe = false;
String last_ir = "none";
void loop()
{
    if (irrecv.decode(&results))
    {

        String str = String((int)results.value, HEX);
        str_msg.data = str.c_str();
        chatter.publish(&str_msg);
        last_ir = str;
        irrecv.resume();
        qwe = true;
        i_count = 0;
    }
    else if (qwe)
    {
        // if (i_count < 1)
        // {
        //     str_msg.data = last_ir.c_str();
        //     chatter.publish(&str_msg);
        //     i_count++;
        // }
        // else
        // {
        //     qwe = false;
        //     i_count = 0;
        // }
    }
    else
    {
        str_msg.data = "none";
        chatter.publish(&str_msg);
    }
    nh.spinOnce();
    delay(300);
}
