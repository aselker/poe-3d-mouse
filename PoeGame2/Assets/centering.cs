using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class centering : MonoBehaviour
{
    public Transform target;
    Quaternion origin;
    public float speed;
    private void Start()
    {
        Quaternion origin = new Quaternion(0,0,0,1);
}
    void Update()
    {
        float step = speed * Time.deltaTime;

        transform.rotation = Quaternion.RotateTowards(transform.rotation, origin, 1);
    }
}