using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO.Ports;
public class PlayerController : MonoBehaviour
{
 
    public float speed;
    private Rigidbody player;
    public string data = "";
    public string stewartPosition = "";
    public Transform target;
    SerialPort serial = new SerialPort("COM6", 115200);
    public float[] stewartInput = new float[6];
 

    // Use this for initialization
    void Start()
    {
        player = GetComponent<Rigidbody>();
        
    }
    void FixedUpdate()
    {

        //movingData(stewartInput);
        moving();
       // rotating(stewartInput);
        output();
        breakjoint();
        writeToArduino();

    }
    void Update()
    {
        if (!serial.IsOpen)
        {
            serial.Open();

        }
        if (serial.IsOpen)
        {
              stewartPosition = readarduino(); // reads poistion and angles from arduino
            stewartInput = readStewartPosition(stewartPosition);
        }
         serial.ReadTimeout = 500;
         serial.WriteTimeout = 500;


    }
    void LateUpdate()
    {
        limitAngle();
    }

    void OnCollisionStay(Collision other)
    {
        
        if (other.rigidbody)
        {
            
            if (Input.GetKeyDown(KeyCode.Space))
            {
                var joint = gameObject.AddComponent<FixedJoint>();
                joint.connectedBody = other.rigidbody;
            }

        }
    }
    void limitAngle()
    {
        float z =player.transform.rotation[1];
        float x = player.transform.rotation[2];
        float y = player.transform.rotation[0];
// float vary = (Mathf.Clamp(y, -0.40f,0.4f));
// float varz = (Mathf.Clamp(z, -0.4f, 0.4f));
// float varx = (Mathf.Clamp(x, -0.4f, 0.4f));
        data = player.transform.rotation[0].ToString("F4")+","+player.transform.rotation[1].ToString("F4")+","+(player.transform.rotation[2]+1).ToString("F4")+","+player.transform.rotation[3].ToString("F4");
        print(data);
        player.transform.rotation = new Quaternion(y, z, x, player.transform.rotation[3]);
        

    }
    void rotating(float[] moredata)
    {
        Quaternion stewartAngles = Quaternion.Euler(moredata[3], moredata[4], moredata[5]);
        float targetx = stewartAngles[2];
        float targety = stewartAngles[0];
        float targetz = stewartAngles[1];

        float z = player.transform.rotation[1];
        float x = player.transform.rotation[2];
        float y = player.transform.rotation[0];

        float torquex = (targetx - x)*50;
        float torquez = (targetz - z)*50;
        float torquey = (targety - y)*50;


        player.GetComponent<Rigidbody>().AddTorque(torquey, torquez, torquex);
    }
    void movingData(float[] moredata)
    {
        Vector3 stewartpos = new Vector3(moredata[0], moredata[1], moredata[2]);
        float targetx = stewartpos[2];
        float targety = stewartpos[0];
        float targetz = stewartpos[1];

        float z = player.transform.position[1];
        float x = player.transform.position[2];
        float y = player.transform.position[0];

        float forcex = (targetx - x) * 50;
        float forcez = (targetz - z) * 50;
        float forcey = (targety - y) * 50;


        player.GetComponent<Rigidbody>().AddForce(forcey, forcez, forcex);
    }
    void moving()
    {

        float moveHorizontal = Input.GetAxis("Horizontal");
        float moveVertical = Input.GetAxis("Vertical");
        float moveUp = 0;

        if (Input.GetKey(KeyCode.Z))
        {
            moveUp = 2;
        }
        if (Input.GetKey(KeyCode.X))
        {
            moveUp = -1;
        }

        Vector3 movement = new Vector3(moveHorizontal, moveUp, moveVertical);
        player.AddForce(movement * 10 - player.velocity);
    }
    void output()
    {
        Vector3 bar = transform.position;
        Vector3 bar2 = transform.eulerAngles;
        data = bar[0].ToString("F2") + "," + bar[1].ToString("F2") + "," + bar[2].ToString("F2") + "," + bar2[0].ToString("F0") + "," + bar[1].ToString("F0") + "," + bar[2].ToString("F0") + "," + Time.fixedDeltaTime + "\r\n";
        //System.IO.File.AppendAllText(@"C:\Users\hyoung\Documents\_POE\POE Project\PoeGame2\data.txt", data);

        Debug.Log(data);
    }

    void breakjoint()
    {
        if (Input.GetKeyDown(KeyCode.D))
        {
            var joint = gameObject.GetComponent<FixedJoint>();
            DestroyObject(joint);

        }
    }
    string readarduino()
    {
        string arduinoData = "not working";
        arduinoData = (string)(serial.ReadLine());
        return arduinoData;
    }

    float[]  readStewartPosition(string input)
    {
        
        float[] stewartData = new float[6];
        string[] temp;

        temp = input.Split(',');
        for( int i = 0; i < 6; i++)
        {
            stewartData[i] = float.Parse(temp[i]);
        }
       // print(stewartData);
  //      Vector3 stewartLocation = new Vector3(stewartData[0], stewartData[1], stewartData[2]);
 //       Quaternion stewartAngles = Quaternion.Euler(stewartData[3], stewartData[4], stewartData[5]);
        
        return stewartData;


    }
    void writeToArduino()
    {
        Vector3 bar = player.transform.position;
        Vector3 bar2 = player.transform.eulerAngles;

       string outPutData = bar[0].ToString("F2") + "," + bar[1].ToString("F2") + "," + bar[2].ToString("F2") + "," + bar2[0].ToString("F0") + "," + bar[1].ToString("F0") + "," + bar[2].ToString("F0")  + "\r\n";
        serial.WriteLine(outPutData);
    }


}

	

