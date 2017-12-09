using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO.Ports;

public class PlayerController : MonoBehaviour
{
   
 
    public float speed;
    private Rigidbody player;
    public string data = "";
    public string send_data = "";
    public string stewartPosition = "";
    public Transform target;
    SerialPort serial = new SerialPort("COM6", 115200);
    public float[] stewartInput = new float[6];
 

    // Use this for initialization
    void Start()
    {
        player = GetComponent<Rigidbody>();
        GameObject thePlayer = GameObject.Find("player");
        networkSocket networkScript = thePlayer.GetComponent<networkSocket>();
       
        

    }
    void FixedUpdate()
    {
       
       // moving();
       // rotating(stewartInput);
        output();
        breakjoint();
        writeToPython(normalVector());

        string actualPosition = GetComponent<networkSocket>().actualPosition;
        string[] positionVectors = actualPosition.Split(',');
        Vector3 xyzPos = new Vector3(float.Parse(positionVectors[0]), float.Parse(positionVectors[1]), float.Parse(positionVectors[2]));
        movingData(xyzPos);


    }
    void Update()
    {
       
      

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
        float vary = (Mathf.Clamp(y, -0.10f,0.1f));
        float varz = (Mathf.Clamp(z, -0.1f, 0.1f));
        float varx = (Mathf.Clamp(x, -0.1f, 0.1f));
        data = player.transform.rotation[0].ToString("F4")+","+player.transform.rotation[1].ToString("F4")+","+(player.transform.rotation[2]+1).ToString("F4")+","+player.transform.rotation[3].ToString("F4");
        print(data);
        player.transform.rotation = new Quaternion(vary, varz, varx, player.transform.rotation[3]);
        

    }
    Vector3 normalVector()
    {
        float z = player.transform.eulerAngles[1];
        float x = player.transform.eulerAngles[2];
        float y = player.transform.eulerAngles[0];

        Vector3 a = transform.TransformPoint(Vector3.Scale(transform.localScale / 2, new Vector3(1, 1, -1)));
        Vector3 b = transform.TransformPoint(Vector3.Scale(transform.localScale / 2, new Vector3(-1, 1, 1)));
        Vector3 c = transform.TransformPoint(Vector3.Scale(transform.localScale / 2, new Vector3(-1, 1, -1)));
        Vector3 side1 = b - a;
        Vector3 side2 = c - a;
        Vector3 perp = Vector3.Cross(side2, side1);
        var perpLength = perp.magnitude;
        perp /= perpLength;

        return (perp);
    

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
    void movingData(Vector3 xyzPos)
    {
      
        float targetx = xyzPos[0];
        float targety = xyzPos[1];
        float targetz = xyzPos[2];
        targetz = targetz - 3;

        float z = player.transform.position[1];
        float x = player.transform.position[2];
        float y = player.transform.position[0];

        float forcex = (targetx - x) * 50;
        float forcez = (targetz - z) * 50;
        float forcey = (targety - y) * 50;

        Debug.Log(xyzPos);
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
    void writeToPython(Vector3 normVec)
    {
        Vector3 bar = player.transform.position;
        Vector3 bar2 = player.transform.eulerAngles;

       string outPutData = bar[0].ToString("F2") + "," + bar[2].ToString("F2") + "," + (bar[1]+3).ToString("F2") + "," + normVec[0].ToString("F0") + "," + normVec[2].ToString("F0") + "," + normVec[1].ToString("F0") + ",";
        send_data = outPutData;
      //  serial.WriteLine(outPutData);
    }



}

	

