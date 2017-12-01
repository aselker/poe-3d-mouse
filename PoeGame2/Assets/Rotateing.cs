using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rotateing : MonoBehaviour {

    public float torque;
    public Rigidbody rb;
    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }
    void FixedUpdate()
    {
      //  float turn = Input.GetAxis("Horizontal");
        rb.AddTorque(transform.up * torque * 1);
    }
}