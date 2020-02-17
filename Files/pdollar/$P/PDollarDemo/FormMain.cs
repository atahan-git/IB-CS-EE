using System;
using System.Collections.Generic;
using System.IO;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using PDollarGestureRecognizer;

namespace PDollarDemo
{
    public partial class FormMain : Form
    {
        List<PDollarGestureRecognizer.Point> points = new List<PDollarGestureRecognizer.Point>();   // mouse points acquired from the user
        Gesture[] trainingSet = null;   // training set loaded from XML files

        #region form constructor

        public FormMain()
        {
            InitializeComponent();
            trainingSet = LoadTrainingSet();
            cbGestureNames.SelectedIndex = 0;
            pbDrawingArea.Image = new Bitmap(pbDrawingArea.Width, pbDrawingArea.Height);
            DrawGesture();
        }

        #endregion

        #region draw gestures

        /// <summary>
        /// Draws a multistroke gesture as connected lines
        /// </summary>
        private void DrawGesture()
        {
            Graphics graphics = null;
            Pen pen = null;
            try
            {
                graphics = Graphics.FromImage(pbDrawingArea.Image);
                graphics.InterpolationMode = System.Drawing.Drawing2D.InterpolationMode.Bicubic;
                graphics.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
                pen = new Pen(Color.OrangeRed, 3);

                // clear canvas
                graphics.Clear(Color.Wheat);

                // draw gesture points
                for (int i = 1; i < points.Count; i++)
                    if (points[i].StrokeID == points[i - 1].StrokeID)
                        graphics.DrawLine(pen, new PointF(points[i - 1].X, points[i - 1].Y), new PointF(points[i].X, points[i].Y));
            }
            finally
            {
                if (pen != null)
                    pen.Dispose();
                if (graphics != null)
                    graphics.Dispose();
                pbDrawingArea.Refresh();
            }
        }

        #endregion

        #region capture and recognize mouse gesture input

        private bool isMouseDown = false;
        private int strokeIndex = -1;
        private void pbDrawingArea_MouseDown(object sender, MouseEventArgs e)
        {
            switch (e.Button)
            {
                case MouseButtons.Left:
                    if (strokeIndex == -1)
                        points = new List<PDollarGestureRecognizer.Point>();
                    isMouseDown = true;
                    strokeIndex++;
                    break;
                case MouseButtons.Right:
                    RecognizeGesture();
                    strokeIndex = -1;
                    break;
            }
        }

        private void pbDrawingArea_MouseUp(object sender, MouseEventArgs e)
        {
            isMouseDown = false;
        }

        private void pbDrawingArea_MouseMove(object sender, MouseEventArgs e)
        {
            if (!isMouseDown) 
                return;
            points.Add(new PDollarGestureRecognizer.Point(e.X, e.Y, strokeIndex));
            DrawGesture();
        }

        private void RecognizeGesture()
        {
            Gesture candidate = new Gesture(points.ToArray());
            string gestureClass = PointCloudRecognizer.Classify(candidate, trainingSet);
            MessageBox.Show("Recognized as: " + gestureClass);
        }

        #endregion

        #region gesture input/output

        /// <summary>
        /// Loads training gesture samples from XML files
        /// </summary>
        /// <returns></returns>
        private Gesture[] LoadTrainingSet()
        {
            List<Gesture> gestures = new List<Gesture>();
            string[] gestureFolders = Directory.GetDirectories(Application.StartupPath + "\\GestureSet");
            foreach (string folder in gestureFolders)
            {
                string[] gestureFiles = Directory.GetFiles(folder, "*.xml");
                foreach (string file in gestureFiles)
                    gestures.Add(GestureIO.ReadGesture(file));
            }
            return gestures.ToArray();
        }

        /// <summary>
        /// Save gesture of existing class to file
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnAddExistingType_Click(object sender, EventArgs e)
        {
            SaveGesture(cbGestureNames.Items[cbGestureNames.SelectedIndex].ToString());
        }

        /// <summary>
        /// Save gesture of new class to file
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnAddNewType_Click(object sender, EventArgs e)
        {
            string gestureName = tbGestureName.Text.Trim();
            if (gestureName.Length == 0)
            {
                MessageBox.Show("Please enter a valid gesture (file) name.", "Info");
                return;
            }
            char[] invalidChars = Path.GetInvalidFileNameChars();
            foreach (char c in gestureName)
                if (invalidChars.Contains(c))
                {
                    MessageBox.Show("Please enter a valid gesture (file) name.", "Info");
                    return;
                }
            SaveGesture(gestureName);
        }

        /// <summary>
        /// Save gesture points to file
        /// </summary>
        /// <param name="fileName"></param>
        private void SaveGesture(string gestureName)
        {
            if (points.Count == 0) 
                return;
            if (!Directory.Exists(Application.StartupPath + "\\GestureSet\\NewGestures"))
                Directory.CreateDirectory(Application.StartupPath + "\\GestureSet\\NewGestures");
            GestureIO.WriteGesture(
                points.ToArray(), 
                gestureName, 
                String.Format("{0}\\GestureSet\\NewGestures\\{1}-{2}.xml", Application.StartupPath, gestureName, DateTime.Now.ToFileTime())
            );

            // reload the training set
            this.trainingSet = LoadTrainingSet();
        }

        /// <summary>
        /// Removes user-defined gestures
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnDelete_Click(object sender, EventArgs e)
        {
            if (Directory.Exists(Application.StartupPath + "\\GestureSet\\NewGestures"))
            {
                string[] files = Directory.GetFiles(Application.StartupPath + "\\GestureSet\\NewGestures");
                foreach (string file in files)
                    File.Delete(file);
            }
                
            // reload the training set
            this.trainingSet = LoadTrainingSet();
        }

        #endregion
    }
}