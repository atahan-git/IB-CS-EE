namespace PDollarDemo
{
    partial class FormMain
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.lblMouseInputInfo = new System.Windows.Forms.Label();
            this.pbGestureSet = new System.Windows.Forms.PictureBox();
            this.pbDrawingArea = new System.Windows.Forms.PictureBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.cbGestureNames = new System.Windows.Forms.ComboBox();
            this.tbGestureName = new System.Windows.Forms.TextBox();
            this.btnAddExistingType = new System.Windows.Forms.Button();
            this.btnAddNewType = new System.Windows.Forms.Button();
            this.label3 = new System.Windows.Forms.Label();
            this.btnDelete = new System.Windows.Forms.Button();
            this.label4 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.pbGestureSet)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pbDrawingArea)).BeginInit();
            this.SuspendLayout();
            // 
            // lblMouseInputInfo
            // 
            this.lblMouseInputInfo.AutoSize = true;
            this.lblMouseInputInfo.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblMouseInputInfo.Location = new System.Drawing.Point(385, 9);
            this.lblMouseInputInfo.Name = "lblMouseInputInfo";
            this.lblMouseInputInfo.Size = new System.Drawing.Size(392, 16);
            this.lblMouseInputInfo.TabIndex = 1;
            this.lblMouseInputInfo.Text = "Make strokes on this canvas. Right-click the canvas to recognize.";
            // 
            // pbGestureSet
            // 
            this.pbGestureSet.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.pbGestureSet.Image = global::PDollarDemo.Properties.Resources.multistrokes;
            this.pbGestureSet.Location = new System.Drawing.Point(12, 28);
            this.pbGestureSet.Name = "pbGestureSet";
            this.pbGestureSet.Size = new System.Drawing.Size(370, 380);
            this.pbGestureSet.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pbGestureSet.TabIndex = 2;
            this.pbGestureSet.TabStop = false;
            // 
            // pbDrawingArea
            // 
            this.pbDrawingArea.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.pbDrawingArea.Location = new System.Drawing.Point(388, 28);
            this.pbDrawingArea.Name = "pbDrawingArea";
            this.pbDrawingArea.Size = new System.Drawing.Size(470, 380);
            this.pbDrawingArea.TabIndex = 0;
            this.pbDrawingArea.TabStop = false;
            this.pbDrawingArea.MouseDown += new System.Windows.Forms.MouseEventHandler(this.pbDrawingArea_MouseDown);
            this.pbDrawingArea.MouseMove += new System.Windows.Forms.MouseEventHandler(this.pbDrawingArea_MouseMove);
            this.pbDrawingArea.MouseUp += new System.Windows.Forms.MouseEventHandler(this.pbDrawingArea_MouseUp);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(385, 415);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(200, 16);
            this.label1.TabIndex = 3;
            this.label1.Text = "Add as exemple of existing type:";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(385, 443);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(198, 16);
            this.label2.TabIndex = 4;
            this.label2.Text = "Add as exemple of custom type:";
            // 
            // cbGestureNames
            // 
            this.cbGestureNames.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cbGestureNames.FormattingEnabled = true;
            this.cbGestureNames.Items.AddRange(new object[] {
            "T",
            "N",
            "D",
            "P",
            "line",
            "five point star",
            "null",
            "arrowhead",
            "X",
            "H",
            "I",
            "exclamation",
            "pitchfork",
            "six point star",
            "asterisk",
            "half note"});
            this.cbGestureNames.Location = new System.Drawing.Point(591, 414);
            this.cbGestureNames.Name = "cbGestureNames";
            this.cbGestureNames.Size = new System.Drawing.Size(98, 21);
            this.cbGestureNames.TabIndex = 5;
            // 
            // tbGestureName
            // 
            this.tbGestureName.Location = new System.Drawing.Point(591, 443);
            this.tbGestureName.Name = "tbGestureName";
            this.tbGestureName.Size = new System.Drawing.Size(98, 20);
            this.tbGestureName.TabIndex = 6;
            // 
            // btnAddExistingType
            // 
            this.btnAddExistingType.Location = new System.Drawing.Point(695, 413);
            this.btnAddExistingType.Name = "btnAddExistingType";
            this.btnAddExistingType.Size = new System.Drawing.Size(71, 24);
            this.btnAddExistingType.TabIndex = 7;
            this.btnAddExistingType.Text = "Add";
            this.btnAddExistingType.UseVisualStyleBackColor = true;
            this.btnAddExistingType.Click += new System.EventHandler(this.btnAddExistingType_Click);
            // 
            // btnAddNewType
            // 
            this.btnAddNewType.Location = new System.Drawing.Point(695, 440);
            this.btnAddNewType.Name = "btnAddNewType";
            this.btnAddNewType.Size = new System.Drawing.Size(71, 24);
            this.btnAddNewType.TabIndex = 8;
            this.btnAddNewType.Text = "Add";
            this.btnAddNewType.UseVisualStyleBackColor = true;
            this.btnAddNewType.Click += new System.EventHandler(this.btnAddNewType_Click);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(385, 472);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(198, 16);
            this.label3.TabIndex = 9;
            this.label3.Text = "Delete all user-defined gestures";
            // 
            // btnDelete
            // 
            this.btnDelete.Location = new System.Drawing.Point(695, 467);
            this.btnDelete.Name = "btnDelete";
            this.btnDelete.Size = new System.Drawing.Size(71, 24);
            this.btnDelete.TabIndex = 10;
            this.btnDelete.Text = "Delete";
            this.btnDelete.UseVisualStyleBackColor = true;
            this.btnDelete.Click += new System.EventHandler(this.btnDelete_Click);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(12, 9);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(76, 16);
            this.label4.TabIndex = 11;
            this.label4.Text = "Gesture set";
            // 
            // FormMain
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(868, 496);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.btnDelete);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.btnAddNewType);
            this.Controls.Add(this.btnAddExistingType);
            this.Controls.Add(this.tbGestureName);
            this.Controls.Add(this.cbGestureNames);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.pbGestureSet);
            this.Controls.Add(this.lblMouseInputInfo);
            this.Controls.Add(this.pbDrawingArea);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Name = "FormMain";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "$P Demo";
            ((System.ComponentModel.ISupportInitialize)(this.pbGestureSet)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pbDrawingArea)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.PictureBox pbDrawingArea;
        private System.Windows.Forms.Label lblMouseInputInfo;
        private System.Windows.Forms.PictureBox pbGestureSet;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.ComboBox cbGestureNames;
        private System.Windows.Forms.TextBox tbGestureName;
        private System.Windows.Forms.Button btnAddExistingType;
        private System.Windows.Forms.Button btnAddNewType;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Button btnDelete;
        private System.Windows.Forms.Label label4;
    }
}

