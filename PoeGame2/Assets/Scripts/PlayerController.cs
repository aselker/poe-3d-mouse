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
    private void FixedUpdate()
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
        Vector3 bar = transform.position;
        Vector3 bar2 = transform.eulerAngles;
        data = bar[0].ToString("F2") + "," + bar[1].ToString("F2")+"," + bar[2].ToString("F2") + "," + bar2[0].ToString("F0")+"," + bar[1].ToString("F0") + "," + bar[2].ToString("F0")+"," +Time.fixedDeltaTime+"\r\n";
        System.IO.File.AppendAllText(@"C:\Users\hyoung\Documents\_POE\POE Project\PoeGame2\data.txt", data);
      

        Debug.Log(data);

        if (Input.GetKeyDown(KeyCode.C))
        {
            var joint = gameObject.GetComponent<FixedJoint>();
            DestroyObject(joint);
            
        }


    }
    private void Update()
    {
       

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
}
	

