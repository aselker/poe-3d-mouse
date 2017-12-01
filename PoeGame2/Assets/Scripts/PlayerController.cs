using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
public class PlayerController : MonoBehaviour
{
 
    public float speed;
    private Rigidbody player;
    public string data = "";
     
           
    // Use this for initialization
    void Start()
    {
        player = GetComponent<Rigidbody>();
        
    }
    void FixedUpdate()
    {

        moving();
        rotating();
        output();
        breakjoint();       


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
               float vary = (Mathf.Clamp(y, -0.20f,0.2f));
        float varz = (Mathf.Clamp(z, -0.2f, 0.2f));
        float varx = (Mathf.Clamp(x, -0.2f, 0.2f));
        data = player.transform.rotation[0].ToString("F4")+","+player.transform.rotation[1].ToString("F4")+","+player.transform.rotation[2].ToString("F4")+","+player.transform.rotation[3].ToString("F4");
        print(data);
        player.transform.rotation = new Quaternion(vary, varz, varx, player.transform.rotation[3]);
        

    }
    void rotating()
    {
        float targetx = 0.0f;
        float targety = 0.0f;
        float targetz = 0.01f;

        float z = player.transform.rotation[1];
        float x = player.transform.rotation[2];
        float y = player.transform.rotation[0];

        float torquex = (targetx - x)*50;
        float torquez = (targetz - z)*50;
        float torquey = (targety - y)*50;


        player.GetComponent<Rigidbody>().AddTorque(torquey, torquez, torquex);
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
        System.IO.File.AppendAllText(@"C:\Users\hyoung\Documents\_POE\POE Project\PoeGame2\data.txt", data);

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
   
}

	

