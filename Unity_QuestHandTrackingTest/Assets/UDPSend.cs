using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.IO;

public class UDPSend : MonoBehaviour
{
    public Transform fingerTip;

    private static int localPort;

    // prefs
    private string IP;  // define in init
    public int port;  // define in init

    // "connection" things
    IPEndPoint remoteEndPoint;
    UdpClient client;

    // gui
    string strMessage = "0.1";
    System.DateTime epochStart;
    DateTime dt = DateTime.Now;
    int startTIme;
    public static int startRecording = 3;
    string questMessage;

    // call it from shell (as program)
    private static void Main()
    {
        UDPSend sendObj = new UDPSend();
        sendObj.init();

        // testing via console
        // sendObj.inputFromConsole();

        // as server sending endless
        sendObj.sendEndless(" endless infos \n");

    }
    
    public static bool _threadRunning;
    Thread _thread;

    void Start()
    {
        //// Begin our heavy work on a new thread.
        //_thread = new Thread(ThreadedWork);
        //_thread.Start();


        startTIme = (DateTime.Now).Millisecond;

        init();

        epochStart = new System.DateTime(1970, 1, 1, 0, 0, 0, System.DateTimeKind.Utc);

    }

    void ThreadedWork()
    {
        _threadRunning = true;
        bool workDone = false;

        // This pattern lets us interrupt the work at a safe point if neeeded.
        while (_threadRunning && !workDone)
        {
            int cur_time = (int)(System.DateTime.UtcNow - epochStart).TotalSeconds;

            // Do Work...
            questMessage = fingerTip.position.x.ToString("F4") + "," +
                           fingerTip.position.y.ToString("F4") + "," +
                           fingerTip.position.z.ToString("F4") + "," +
                           cur_time.ToString("F0") + "," +
                           startRecording.ToString("F0");

            //print("Finger tip positions: " + questMessage);

            sendString(questMessage + "\n");
        }
        _threadRunning = false;
    }

    void OnDisable()
    {
        // If the thread is still running, we should shut it down,
        // otherwise it can prevent the game from exiting correctly.
        if (_threadRunning)
        {
            // This forces the while loop in the ThreadedWork function to abort.
            _threadRunning = false;

            // This waits until the thread exits,
            // ensuring any cleanup we do after this is safe. 
            _thread.Join();
        }

        // Thread is guaranteed no longer running. Do other cleanup tasks.
    }

    void Update()
    {
        int cur_time = (int)(System.DateTime.UtcNow - epochStart).TotalSeconds;

        //questMessage = fingerTip.position.x.ToString("F4") + "," +
        //               fingerTip.position.y.ToString("F4") + "," +
        //               fingerTip.position.z.ToString("F4") + "," +
        //               cur_time.ToString("F0") + "," +
        //               startRecording.ToString("F0");   
        
        questMessage = Experiment.fileName + "," +
                       cur_time.ToString("F0") + "," +
                       startRecording.ToString("F0");

        sendString(questMessage + "\n");

    }

    // OnGUI
    void OnGUI()
    {
        Rect rectObj = new Rect(40, 380, 200, 400);
        GUIStyle style = new GUIStyle();
        style.alignment = TextAnchor.UpperLeft;
        GUI.Box(rectObj, "# UDPSend-Data\n127.0.0.1 " + port + " #\n"
                    + "shell> nc -lu 127.0.0.1  " + port + " \n"
                , style);

        // ------------------------
        // send it
        // ------------------------
        strMessage = GUI.TextField(new Rect(160, 360, 140, 20), strMessage);
        if (GUI.Button(new Rect(310, 360, 40, 20), "send"))
        {

            sendString(strMessage + "\n");
        }
    }

    // init
    public void init()
    {
        // Endpunkt definieren, von dem die Nachrichten gesendet werden.
        print("UDPSend.init()");

        // define
        IP = "127.0.0.1";
        //port = 8888;

        // ----------------------------
        // Senden
        // ----------------------------
        remoteEndPoint = new IPEndPoint(IPAddress.Parse(IP), port);
        client = new UdpClient();

        // status
        print("Sending to " + IP + " : " + port);
        print("Testing: nc -lu " + IP + " : " + port);

    }

    byte[] BinarySystem(string message)
    {
        var str = new MemoryStream();
        var bw = new BinaryWriter(str);
        //bw.Write(42);
        bw.Write(message);

        var bytes = str.ToArray();

        return bytes;
    }

    // sendData
    private void sendString(string message)
    {
        try
        {
            //float mess = float.Parse(message);

            // Daten mit der UTF8-Kodierung in das Binärformat kodieren.
            //byte[] data = BitConverter.GetBytes(mess);
            byte[] data = Encoding.UTF8.GetBytes(message);
            //byte[] data = BinarySystem(message);

            // Den message zum Remote-Client senden.
            client.Send(data, data.Length, remoteEndPoint);
            //Debug.Log("Sending length: " + data.Length);
            //            Debug.Log("Tx : " + message);

        }
        catch (Exception err)
        {
            print(err.ToString());
        }
    }

    // endless test
    private void sendEndless(string testStr)
    {
        do
        {
            sendString(testStr);
        }
        while (true);

    }

}
