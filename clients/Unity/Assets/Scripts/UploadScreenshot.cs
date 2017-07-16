using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;


public class UploadScreenshot : MonoBehaviour {

    Camera captureCamera;

    public bool capture = false;
    byte[] bytes;

    //string imageUploadURL = "http://127.0.0.1:5000/upload";
    //public string imageUploadURL = "http://192.168.2.255:5000/upload";
    string imageUploadURL = "http://192.168.0.2:5000/upload"; 
	// Use this for initialization

    public  Text text;

    public string sceneName;


    int     buildNumber;
    string  deviceName;

    int _temp = 0;


    void Start () {
        
        captureCamera = GetComponent<Camera>();
        deviceName = SystemInfo.deviceName;
        char[] charsToTrim = { ' ', '\t' };
        deviceName = deviceName.Trim(charsToTrim);

        Debug.Log(captureCamera);


	}
	
	
    void TakeScreenShot(){

        //Texture2D tex = new Texture2D(
        RenderTexture currentActiveRT = RenderTexture.active;

        RenderTexture rt = new RenderTexture(captureCamera.pixelWidth, captureCamera.pixelHeight, 24, RenderTextureFormat.ARGB32 );
        captureCamera.targetTexture = rt;
       
        captureCamera.Render();
        RenderTexture.active = rt;

        Texture2D tex = new Texture2D(rt.width, rt.height, TextureFormat.ARGB32, false);


        tex.ReadPixels(new Rect(0, 0, rt.width, rt.height), 0, 0);
        tex.Apply();
        captureCamera.targetTexture = null;
        RenderTexture.active = currentActiveRT;

        bytes = tex.EncodeToPNG();
        //Debug.Log("Captured");

        StartCoroutine(UploadScreenShot());


    }

    void Update() {
        if(!capture) {
            if (Input.GetMouseButtonDown(0)){
                GrabAndUploadScreenshot(6);
                capture = true;
            }
        }
    }

    public bool GrabAndUploadScreenshot(int _buildNumber) {
        buildNumber = _buildNumber;
        buildNumber = _temp;
        _temp += 1;
        TakeScreenShot();
        return true;
    
    }



   

    IEnumerator UploadScreenShot() {

        var form = new WWWForm();
        form.AddField("frameCount", Time.frameCount.ToString());
        string filename = "screenShot_"+ buildNumber + "_" + deviceName+ "_" + sceneName +".png";
        form.AddBinaryData("file", bytes, filename, "image/png");
        Debug.Log("Uploading: " + filename);

        //text.text = "before req";
        UnityWebRequest www = UnityWebRequest.Post(imageUploadURL, form);
        //text.text = "before send";
        yield return www.Send();
        if(www.isError) {
            text.text = www.error;
        }
        else {
            text.text = "Form upload complete!";

        }
        capture = false;





    }

}
