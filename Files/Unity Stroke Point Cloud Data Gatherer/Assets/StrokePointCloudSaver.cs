using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using UnityEngine.UI;
using System;
using System.Runtime.Serialization.Formatters.Binary;
using System.Xml;
using System.Xml.Serialization;

public class StrokePointCloudSaver : MonoBehaviour {
	public GameObject pointPrefab;
	public GameObject strokePrefab;
	Camera mainCam;
	FileInfo f;

	public Text gestureName;
	public Text repCountText;

	public int curGestureGroupIndex = 0;
	public int curGestureIndex = 0;
	public int curStrokeIndex = 0;
	public string[] gestureNames;

	// Start is called before the first frame update
	void Start () {
		mainCam = Camera.main;

		for (int i = 0; i < gestureNames.Length; i++) {
			gestureNames[i] = i.ToString () + "-" + gestureNames[i];
		}

		if (Load ()) {
			if (mySave.gestureSetCount == gestureNames.Length) {
				for (int i = 0; i < gestureNames.Length; i++) {
					if(mySave.GestureSets[i].repetitions.Count <= 0)
						mySave.GestureSets[i].repetitions.Add (new Gesture (gestureNames[i], 0));
				}

				print ("Loaded succesfuly");
			} else {
				SetUpSave ();
			}
		} else {
			SetUpSave ();
		}


		ChangeGesture (0);
	}

	void SetUpSave () {
		for (int i = 0; i < gestureNames.Length; i++) {
			mySave.GestureSets.Add (new GestureSet (gestureNames[i]));
			mySave.GestureSets[i].repetitions.Add (new Gesture (gestureNames[i], 0));
		}

		mySave.gestureSetCount = gestureNames.Length;

		print ("New save set-up");
	}

	bool isDrawing = false;
	Vector3 lastPost = Vector3.zero;
	List<Vector3> lnPos = new List<Vector3> ();
	GameObject curStrokeObj;

	string theGreatSaveString = "";

	// Update is called once per frame
	void Update () {
		//print (Input.mousePosition);

		if (Input.GetMouseButtonDown (0)) {
			if (Input.mousePosition.y > 220 && Input.mousePosition.y < 1920-220) {
				print ("New Stroke");
				isDrawing = true;

				curStrokeObj = Instantiate (strokePrefab, transform);
				if (mySave.GestureSets[curGestureGroupIndex].repetitions.Count <= curGestureIndex)
					NewRepetition ();

				mySave.GestureSets[curGestureGroupIndex].repetitions[curGestureIndex].strokes.Add (new Gesture.Stroke (curStrokeIndex));

				mySave.GestureSets[curGestureGroupIndex].repetitions[curGestureIndex].strokeCount = curStrokeIndex+1;
			}
		}

		if (isDrawing && Vector3.Distance (lastPost, Input.mousePosition) > 1f) {
			GameObject p = Instantiate (pointPrefab, curStrokeObj.transform);
			p.transform.position = mainCam.ScreenToWorldPoint (Input.mousePosition);
			p.transform.position += Vector3.forward * 10;
			lnPos.Add (p.transform.position + Vector3.forward);
			curStrokeObj.GetComponent<LineRenderer>().positionCount = lnPos.Count;
			curStrokeObj.GetComponent<LineRenderer>().SetPositions (lnPos.ToArray());

			mySave.GestureSets[curGestureGroupIndex].repetitions[curGestureIndex]
				.strokes[curStrokeIndex].points.Add (new Gesture.Point (p.transform.position, Time.realtimeSinceStartup));

			mySave.GestureSets[curGestureGroupIndex].repetitions[curGestureIndex]
				.strokes[curStrokeIndex].pointCount = lnPos.Count;
		}

		if (isDrawing && Input.GetMouseButtonUp (0)) {
			print ("Finished Drawing");

			isDrawing = false;

			lnPos = new List<Vector3> ();
			curStrokeIndex++;
		}
	}

	public void ChangeGesture (int c) {
		curGestureGroupIndex += c;
		curGestureGroupIndex = Mathf.Clamp (curGestureGroupIndex, 0, gestureNames.Length-1);
		gestureName.text = gestureNames[curGestureGroupIndex];
		curGestureIndex = mySave.GestureSets[curGestureGroupIndex].repetitions.Count - 1;

		if (curGestureIndex < 0)
			NewRepetition ();

		repCountText.text = "Next Repetition\n" + (curGestureIndex).ToString () + "/50";
	}

	public void DeleteLastShape () {
		ClearGfxs ();
		mySave.GestureSets[curGestureGroupIndex].repetitions.RemoveAt (curGestureIndex);
		curGestureIndex--;

		NewRepetition ();
	}

	public void NewRepetition () {
		curGestureIndex++;
		ClearGfxs ();
		mySave.GestureSets[curGestureGroupIndex].repetitions.Add (new Gesture (mySave.GestureSets[curGestureGroupIndex].GroupName, curGestureIndex));
		curStrokeIndex = 0;

		mySave.GestureSets[curGestureGroupIndex].repetitionCount = curGestureIndex;
		repCountText.text = "Next Repetition\n" + (curGestureIndex).ToString () + "/50";
	}

	void ClearGfxs () {
		int childCount = transform.childCount;
		for (int i = childCount - 1; i >= 0; i--) {
			Destroy (transform.GetChild (i).gameObject);
		}
	}

	public void SavetoFile () {

		//mySave.GestureSets[curGestureGroupIndex].repetitions.RemoveAt (curGestureIndex);

		Save (mySave);

		//mySave.GestureSets[curGestureGroupIndex].repetitions.Add (new Gesture (mySave.GestureSets[curGestureGroupIndex].GroupName, curGestureIndex));
		print ("Save success >> " + path);
	}


	string saveName = "GesturesSave";
	public SaveData mySave = new SaveData ();

	string path { get { return Path.Combine (Application.persistentDataPath, 
		(System.DateTime.Now.ToString ()).Replace ("/", "-").Replace (':', '-').Replace (" ", "--") + " " + 
		saveName + ".xml"); } }

	string lastSavePath {
		get {
			return Path.Combine (Application.persistentDataPath, "LastSave" + ".xml");
		}
	}

	void Awake () {
		//Load ();
		print ("Save Data Location: " + path);
	}

	void Save (SaveData toSave) {
		var serializer = new XmlSerializer (typeof (SaveData));
		var stream = new FileStream (path, FileMode.Create);
		serializer.Serialize (stream, toSave);
		stream.Close ();

		serializer = new XmlSerializer (typeof (SaveData));
		stream = new FileStream (lastSavePath, FileMode.Create);
		serializer.Serialize (stream, toSave);
		stream.Close ();
	}

	public bool Load () {
		try {
			if (File.Exists (lastSavePath)) {
				var serializer = new XmlSerializer (typeof (SaveData));
				var stream = new FileStream (lastSavePath, FileMode.Open);
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


[Serializable]
[XmlRoot ("Save Data")]
public class SaveData {

	public int gestureSetCount = 0;

	public List<GestureSet> GestureSets = new List<GestureSet> ();
}

public class GestureSet {
	[XmlAttribute ("GroupName")]
	public string GroupName = "defName";

	public List<Gesture> repetitions = new List<Gesture> ();

	[XmlAttribute ("RepetitionCount")]
	public int repetitionCount = 0;

	public GestureSet () { }
	public GestureSet (string _GroupName) {
		GroupName = _GroupName;
	}
}


[Serializable]
public class Gesture {
	[XmlAttribute("GestureName")]
	public string Name = "defName";

	[XmlAttribute ("RepetitionIndex")]
	public int repetitionIndex = 0;
	public List<Stroke> strokes = new List<Stroke> ();

	[XmlAttribute ("StrokeCount")]
	public int strokeCount = 0;

	[Serializable]
	public class Stroke {
		[XmlAttribute ("Index")]
		public int index = 0;
		[XmlAttribute ("PointCount")]
		public int pointCount = 0;

		public List<Point> points = new List<Point> ();

		public Stroke () { }
		public Stroke (int _index) {
			index = _index;
		}
	}

	[Serializable]
	public class Point {
		[XmlAttribute]
		public float x, y, t;

		public Point () { }

		public Point (Vector3 p, float time) {
			x = p.x;
			y = p.y;
			t = time;
		}
	}

	public Gesture () { }
	public Gesture (string _Name, int _index) {
		Name = _Name;
		repetitionIndex = _index;
	}
}
