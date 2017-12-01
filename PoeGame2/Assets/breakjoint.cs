using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class breakjoint : MonoBehaviour {

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
        

            var joint = gameObject.GetComponent<FixedJoint>();
            if (Input.GetKeyDown(KeyCode.D))
            {
                Destroy(joint);
            }
        }

    
}
