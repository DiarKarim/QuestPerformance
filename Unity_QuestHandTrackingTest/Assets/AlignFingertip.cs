using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AlignFingertip : MonoBehaviour
{
    public Transform virtualFingerTip;
    public Transform MarkerTip;
    public Transform StartMarker;
    public Transform MarkerTable;


    public void Align()
    {
        // Reposition virtual fingertip to real fingertip (marker)
        Vector3 offset = MarkerTip.position - virtualFingerTip.position;
        transform.position = transform.position + offset;

        // Reposition virtual fingertip to start marker 
        Vector3 offset2Start = virtualFingerTip.position - StartMarker.position;
        MarkerTable.position = MarkerTable.position + offset2Start;
    }

    void Update()
    {
        //if(Input.GetKeyDown(KeyCode.A))
        //{
        //    Align();
        //}
    }
}
