import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.FileDialog;
import java.awt.GridLayout;
import java.awt.Image;
import java.awt.Rectangle;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;
import java.awt.image.BufferedImage;
import java.awt.image.MemoryImageSource;
import java.awt.image.PixelGrabber;
import java.io.File;

import javax.imageio.ImageIO;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JSlider;
import javax.swing.KeyStroke;
import javax.swing.border.EmptyBorder;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

/*
 * Nathan Floor
 * FLRNAT001
 * 
 * Hough Feature Detector Transform
 * GUI class for interface
 * Using Java swing
 * 
 */

public class MainWindow extends JFrame{	
	private static final long serialVersionUID = 1L;
	
	private BufferedImage inputImage; 
	private ImagePanel outputImagePnl;
	private ImagePanel accImagePnl;
	private ImagePanel inputImagePnl;
	private JProgressBar statusBar;
	private JButton btnProcess;
	private JSlider sldCircles;
	private RangeSlider sldRadius;
	private JLabel lblRadius;
	private JLabel lblCircles;
	
	private EdgeDetector edgeDetector;
	private Thresholder thresholder;
	private HoughCircleTransform houghDetector;
	private JFrame parent;
	private String status = "Chillin";
	
	private int numCircles = 1;

	public MainWindow(){
		super("ICV Hough Transform");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 30, 600, 500);
		
		//setup menu
		JMenuBar menuBar = new JMenuBar();
		setJMenuBar(menuBar);
		
		//File menu dropdown
		JMenu mnFile = new JMenu("File");
		menuBar.add(mnFile);
		
		JMenuItem openFile = new JMenuItem("Open");
		openFile.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_O, InputEvent.CTRL_MASK));
		openFile.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent arg0) {
				//open file dialog
				FileDialog openFile = new FileDialog(parent);
				openFile.setMode(FileDialog.LOAD);
				openFile.setFile("images/image.gif");
				openFile.setVisible(true);
				try{
					System.out.println(openFile.getDirectory()+openFile.getFile());
					inputImage = ImageIO.read(new File(openFile.getDirectory()+openFile.getFile()));
					inputImagePnl.setImage(inputImage);
					inputImagePnl.repaint();
					btnProcess.setEnabled(true);
				}catch(Exception e){
					e.printStackTrace();
				}
				System.out.println("Image successfully read-in...");
			}
		});
		mnFile.add(openFile);
		
		JMenuItem exitItem = new JMenuItem("Exit");
		exitItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_Q, InputEvent.CTRL_MASK));
		exitItem.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent arg0) {
				System.exit(0);				
			}
		});
		mnFile.add(exitItem);
		
		//setup layout managers
		setLayout(new BorderLayout());
		
		JPanel processPanel = new JPanel();
		processPanel.setLayout(new GridLayout(3,1));
		
		btnProcess = new JButton("Process");
		btnProcess.setEnabled(false);
		btnProcess.addActionListener(new ActionListener() {			
			@Override
			public void actionPerformed(ActionEvent arg0) {			
				int width = inputImage.getWidth();
				int height = inputImage.getHeight();
				
				int[] original = new int[width*height];
				PixelGrabber pixelGrabber = new PixelGrabber(inputImage, 0, 0, width, height, original, 0, width);
				try{
					pixelGrabber.grabPixels();
				}catch(InterruptedException e){
					e.printStackTrace();
				}
				lblCircles.setText("Number of circles: "+sldCircles.getValue());
				lblRadius.setText("Circle Radius: "+sldRadius.getValue());
				
				// detect edges						
				status = "Edge Detection";
				edgeDetector = new EdgeDetector(original, width, height);
				int[] edges = new int[width*height];
				edges = edgeDetector.detectEdges();
								
				//thresholding
				status = "Thresholding";
				thresholder = new Thresholder(edges, width, height);
				int[] thresh = new int[width*height];
				thresh = thresholder.process();
												
				// Hough transform	
				status = "Processing";
				houghDetector = new HoughCircleTransform(thresh, width, height, sldCircles.getValue());
				Image newLayer = null;
				int[] temp = new int[width*height];
				int[] hough = new int[width*height];
				int count = 0;
				for(int r=sldRadius.getValue();r<sldRadius.getUpperValue();r+=5){
					Monitor progress3 = new Monitor((ProgressMonitor)houghDetector);
					progress3.start();
					hough = houghDetector.detectCircles(r);
					if(count==0)
						temp = layerOriginalImage(original, hough);
					else
						temp = layerOriginalImage(temp, hough);
					newLayer=createImage(new MemoryImageSource(width, height, temp, 0, width));
					
					try {
						progress3.join();
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
				}				

				int[] accData = new int[width*height];
				accData = houghDetector.getAcc();	

				Image AccImage = createImage(new MemoryImageSource(width, height, accData, 0, width));
				accImagePnl.setImage(AccImage);
				accImagePnl.repaint();
				 
				outputImagePnl.setImage(newLayer);
				outputImagePnl.repaint();					
			}
		});
		JPanel sliderLabels = new JPanel();
		sliderLabels.setLayout(new GridLayout(1,2));
		processPanel.add(sliderLabels);
		JLabel circleLbl = new JLabel("Number of Circles:");
		sliderLabels.add(circleLbl);
		JLabel radiusLbl = new JLabel("Radius of circles:");
		sliderLabels.add(radiusLbl);
		
		//add sliders for radius and number of circles
		JPanel sliderPnl = new JPanel();
		sliderPnl.setLayout(new GridLayout(1,2));
		sldCircles = new JSlider(JSlider.HORIZONTAL, 1, 50, numCircles);
		sldCircles.addChangeListener(new circlesListener());
		sldCircles.setMajorTickSpacing(10);
		sldCircles.setMinorTickSpacing(5);
		sldCircles.setPaintLabels(true);
		sldCircles.setPaintTicks(true);
		
		sliderPnl.add(sldCircles);	
		sldRadius = new RangeSlider(5, 60);
		sldRadius.setMajorTickSpacing(10);
		sldRadius.setMinorTickSpacing(5);
		sldRadius.setPaintLabels(true);
		sldRadius.setPaintTicks(true);
		sldRadius.setValue(20);
		sldRadius.setUpperValue(40);
		sldRadius.addChangeListener(new radiusListener());
		sliderPnl.add(sldRadius);
		
		processPanel.add(sliderPnl);
		processPanel.add(btnProcess);		
		this.add(processPanel, BorderLayout.NORTH);
		
		//add image panels
		JPanel imagesPanel = new JPanel();
		imagesPanel.setLayout(new GridLayout(1, 3));
		this.add(imagesPanel, BorderLayout.CENTER);
		
		inputImagePnl = new ImagePanel();
		inputImagePnl.setBorder(new EmptyBorder(20, 20, 20, 20));
		imagesPanel.add(inputImagePnl);
		
		accImagePnl = new ImagePanel();
		accImagePnl.setBorder(new EmptyBorder(20, 20, 20, 20));
		imagesPanel.add(accImagePnl);
		
		outputImagePnl = new ImagePanel();
		outputImagePnl.setBorder(new EmptyBorder(100, 100, 100, 100));
		imagesPanel.add(outputImagePnl);
		
		//add save button and loading bar
		JPanel bottomPanel = new JPanel();
		bottomPanel.setLayout(new BorderLayout());
		this.add(bottomPanel, BorderLayout.SOUTH);
	
		JPanel savePanel = new JPanel();
		savePanel.setLayout(new GridLayout(2, 1));
		bottomPanel.add(savePanel, BorderLayout.NORTH);
		
		JPanel imgLabels = new JPanel();
		imgLabels.setLayout(new GridLayout(1,3));
		
		JLabel origlbl = new JLabel("Original Image", JLabel.CENTER);
		imgLabels.add(origlbl);
		origlbl.setForeground(Color.BLUE);
		JLabel accumlbl = new JLabel("Accumulated Img",JLabel.CENTER);
		imgLabels.add(accumlbl);
		accumlbl.setForeground(Color.BLUE);
		JLabel overlaylbl = new JLabel("Circles On Original",JLabel.CENTER);
		imgLabels.add(overlaylbl);
		overlaylbl.setForeground(Color.BLUE);	
		savePanel.add(imgLabels);
		
		JPanel feedbackPnl = new JPanel();
		savePanel.add(feedbackPnl);
		feedbackPnl.setLayout(new GridLayout(1,2));
		lblCircles = new JLabel("Number of circles: "+sldCircles.getValue());
		lblRadius = new JLabel("Circle Radius: max:"+sldRadius.getUpperValue()+" & min:"+sldRadius.getValue());
		feedbackPnl.add(lblRadius);
		feedbackPnl.add(lblCircles);
		
		JPanel statusPanel = new JPanel();
		statusPanel.setLayout(new BorderLayout());
		bottomPanel.add(statusPanel, BorderLayout.SOUTH);
		statusBar = new JProgressBar(0, 100);
		statusBar.setStringPainted(true);
		statusBar.setString("Nothing Happening.");
		statusBar.setValue(0);
		statusBar.setIndeterminate(false);
		statusBar.setEnabled(true);		
		statusPanel.add(statusBar, BorderLayout.CENTER);
		
		System.out.println("Loaded Interface...");
	}

	public BufferedImage getInputImage() {
		return inputImage;
	}
	public void setInputImage(BufferedImage inputImage) {
		this.inputImage = inputImage;
	}
	public JFrame getParent() {
		return parent;
	}
	public void setParent(MainWindow parent) {
		this.parent = parent;
	}
	
	class radiusListener implements ChangeListener{
		@Override
		public void stateChanged(ChangeEvent arg0) {
			JSlider source = (JSlider)arg0.getSource();
			if(!source.getValueIsAdjusting()){				
				lblRadius.setText("Circle Radius: max:"+sldRadius.getUpperValue()+" & min:"+sldRadius.getValue());
			}			
		}		
	}
	class circlesListener implements ChangeListener{
		@Override
		public void stateChanged(ChangeEvent arg0) {
			JSlider source = (JSlider)arg0.getSource();
			if(!source.getValueIsAdjusting()){
				lblCircles.setText("Number of circles: "+sldCircles.getValue());
			}			
		}		
	}
	
	/*
	 * This method writes a layer over the original image.
	 * The new layer is of the circles detected by the hough transform.
	 * Shape Outlines are in red. 
	 * Can place mnay layers on top of each other.
	 */
	private int[] layerOriginalImage(int[] original, int[] new_data) {
		int width = inputImage.getWidth();
		int height = inputImage.getHeight();
		int[] new_img = new int[width*height];
		new_img = original;
		
		for(int x=0;x<width;x++){
			for(int y=0;y<height;y++){
				if((new_data[x+(width*y)] & 0xff) > 0)
					new_img[x+(width*y)] = 0xffff0000; //change colour of circle-shape to red
			}
		}
		
		return new_img;
	}

	//inner class for progressbar monitor thread
	class Monitor extends Thread{
		private ProgressMonitor parent;
		private int max = 0;

		public Monitor(ProgressMonitor p){
			parent = p;

			statusBar.setValue(0);  
			max = parent.getMax();
			statusBar.setMaximum(max);
			Rectangle progressRect = statusBar.getBounds();  
			progressRect.x = 0;  
			progressRect.y = 0;  
			statusBar.paintImmediately( progressRect );
		}
		
		public void run(){			
			int progress = 0;			
			int percent = 0;			
			do{
				progress = parent.getProgressCounter();
				percent = Math.min(Math.round(progress/(float)max*100), 100);
				statusBar.setValue(progress);
				statusBar.setString(status+": "+percent+"%");
				
				Rectangle progressRect = statusBar.getBounds();  
				progressRect.x = 0;  
				progressRect.y = 0;  
				statusBar.paintImmediately( progressRect );  
				
//				System.out.println(max+" "+progress);
				
				if(percent == 100)
					this.interrupt();
			}while(progress < max);
			
			statusBar.setString("Nothing Happening.");
			statusBar.setValue(0);
		}
	}	
}
