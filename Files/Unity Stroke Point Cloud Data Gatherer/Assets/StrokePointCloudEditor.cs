using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using UnityEngine.UI;
using System;
using System.Runtime.Serialization.Formatters.Binary;
using System.Xml;
using System.Xml.Serialization;
using PDollarGestureRecognizer;

public class StrokePointCloudEditor : MonoBehaviour {
	public GameObject pointPrefab;
	public GameObject strokePrefab;
	FileInfo f;

	public Text gestureName;
	public Text repCountText;

	public int curGestureGroupIndex = 0;
	public int curGestureIndex = 0;
	public int curStrokeIndex = 0;
	public string[] gestureNames;

	// Start is called before the first frame update
	void Start () {

		if (Load ()) {
			CleanUp ();
			print ("Loaded succesfuly");

		}

		ChangeGesture (0);
	}

	GameObject curStrokeObj;

	string theGreatSaveString = "";

	public void AutoCycleReps () {
		if (isRunning) {
			StopAllCoroutines ();
			isRunning = false;
		} else {
			StartCoroutine (Cycle ());
			isRunning = true;
		}
	}

	bool isRunning = false;
	IEnumerator Cycle () {
		float timer = 0.3f;
		float shortener = 0.05f;
		float shortest = 0.1f;
		while (true) {
			ChangeRepetiton (1);
			yield return new WaitForSeconds (timer);

			timer -= shortener;
			timer = Mathf.Clamp (timer, shortest, 10);
		}
	}

	public void ChangeGesture (int c) {
		curGestureGroupIndex += c;
		curGestureGroupIndex = Mathf.Clamp (curGestureGroupIndex, 0, mySave.GestureSets.Count-1);
		gestureName.text = mySave.GestureSets[curGestureGroupIndex].GroupName;

		curGestureIndex = 0;

		ChangeRepetiton (0);

	}

	public GameObject loopFlash;
	int capIndex = 0;
	private void Update () {
		if (Input.GetMouseButtonDown (1)) {
			ClearGfxs ();

			List<Point> myPoints = new List<Point> ();

			int strokeId = 0;
			foreach (Gesture.Stroke stroke in mySave.GestureSets[curGestureGroupIndex].repetitions[curGestureIndex].strokes) {
				foreach (Gesture.Point point in stroke.points) {
					myPoints.Add (new Point (point.x, point.y, strokeId));
				}
				strokeId++;
			}

			PDollarGestureRecognizer.Gesture myGesture = new PDollarGestureRecognizer.Gesture (myPoints.ToArray ());

			foreach (Point point in myGesture.Points) {
				GameObject p = Instantiate (pointPrefab, transform);
				p.transform.position = new Vector3 (point.X, point.Y, 0);
			}
		}

		if (Input.GetMouseButtonDown (0)) {
			ScreenCapture.CaptureScreenshot ("Shape " + capIndex.ToString() + ".png");
			capIndex++;
		}
		if(Input.mouseScrollDelta.y != 0)
			ChangeGesture((int)Input.mouseScrollDelta.y);
	}

	public void ChangeRepetiton (int c) {
		curGestureIndex += c;
		if (curGestureIndex > mySave.GestureSets[curGestureGroupIndex].repetitions.Count - 1) {
			curGestureIndex = 0;
			loopFlash.SetActive (true);
		} else {
			loopFlash.SetActive (false);
		}
		curGestureIndex = Mathf.Clamp (curGestureIndex, 0, mySave.GestureSets[curGestureGroupIndex].repetitions.Count-1);

		
		if (mySave.GestureSets[curGestureGroupIndex].repetitions.Count != 0)
			DrawGfxs ();
		

		repCountText.text = "Current Repetition\n" + (curGestureIndex).ToString () + "/50";
	}

	public void DeleteRepetition () {
		mySave.GestureSets[curGestureGroupIndex].repetitions.RemoveAt (curGestureIndex);
		curGestureIndex--;

		ChangeRepetiton (0);

		UpdateCounts ();
	}

	List<Vector3> lnPos = new List<Vector3> ();
	void DrawGfxs () {
		ClearGfxs ();

		foreach (Gesture.Stroke stroke in mySave.GestureSets[curGestureGroupIndex].repetitions[curGestureIndex].strokes) {
			curStrokeObj = Instantiate (strokePrefab, transform);
			lnPos.Clear ();
			foreach (Gesture.Point point in stroke.points) {
				GameObject p = Instantiate (pointPrefab, curStrokeObj.transform);
				p.transform.position = new Vector3 (point.x,point.y, 0);
				lnPos.Add (p.transform.position + Vector3.forward);
			}
			curStrokeObj.GetComponent<LineRenderer> ().positionCount = lnPos.Count;
			curStrokeObj.GetComponent<LineRenderer> ().SetPositions (lnPos.ToArray ());
		}
	}

	void ClearGfxs () {
		int childCount = transform.childCount;
		for (int i = childCount - 1; i >= 0; i--) {
			Destroy (transform.GetChild (i).gameObject);
		}
	}

	void CleanUp () {
		mySave.gestureSetCount = mySave.GestureSets.Count;
		foreach (GestureSet gestureSets in mySave.GestureSets) {
			foreach (Gesture gesture in gestureSets.repetitions) {
				foreach (Gesture.Stroke stroke in gesture.strokes) {
					stroke.points.RemoveAll (point => point.y > 3.8f);
					stroke.points.RemoveAll (point => point == null);
					stroke.pointCount = stroke.points.Count;
				}
				gesture.strokes.RemoveAll (stroke => stroke.pointCount == 0);
				gesture.strokes.RemoveAll (stroke => stroke == null);
				gesture.strokeCount = gesture.strokes.Count;
			}
			gestureSets.repetitions.RemoveAll (gesture => gesture.strokeCount == 0);
			gestureSets.repetitions.RemoveAll (gesture => gesture == null);
			gestureSets.repetitionCount = gestureSets.repetitions.Count;
		}
		
	}

	void UpdateCounts () {
		mySave.gestureSetCount = mySave.GestureSets.Count;
		foreach (GestureSet gestureSets in mySave.GestureSets) {
			foreach (Gesture gesture in gestureSets.repetitions) {
				foreach (Gesture.Stroke stroke in gesture.strokes) {
					stroke.pointCount = stroke.points.Count;
				}
				gesture.strokeCount = gesture.strokes.Count;
			}
			gestureSets.repetitionCount = gestureSets.repetitions.Count;
		}
	}

	public void SavetoFile () {

		//mySave.GestureSets[curGestureGroupIndex].repetitions.RemoveAt (curGestureIndex);

		

		Save (mySave);

		//mySave.GestureSets[curGestureGroupIndex].repetitions.Add (new Gesture (mySave.GestureSets[curGestureGroupIndex].GroupName, curGestureIndex));
		print ("Save success >> " + savePath);
	}


	string saveName = "EditedGestureSave";
	public SaveData mySave = new SaveData ();

	string savePath {
		get {
			return "D:\\_DERS\\IB IAs and EE and CAS\\EE\\Python Dollar\\Edit\\"+
(System.DateTime.Now.ToString ()).Replace ("/", "-").Replace (':', '-').Replace (" ", "--") + " " +
saveName + ".xml";
		}
	}

	string editPath {
		get {
			return "D:\\_DERS\\IB IAs and EE and CAS\\EE\\Python Dollar\\Edit\\EditedData.xml";
		}
	}

	void Awake () {
		//Load ();
		print ("Save Data Location: " + savePath);
	}

	void Save (SaveData toSave) {
		var serializer = new XmlSerializer (typeof (SaveData));
		var stream = new FileStream (savePath, FileMode.Create);
		serializer.Serialize (stream, toSave);
		stream.Close ();
	}

	public bool Load () {
		try {
			if (File.Exists (editPath)) {
				var serializer = new XmlSerializer (typeof (SaveData));
				var stream = new FileStream (editPath, FileMode.Open);
				var container = serializer.Deserialize (stream) as SaveData;
				stream.Close ();

				mySave = container;
				return true;
			} else {
				return false;
			}
		} catch {
			return false;
		}
	}
}