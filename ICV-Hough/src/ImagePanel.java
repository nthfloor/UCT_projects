/*
 * Nathan Floor
 * FLRNAT001
 * 
 * Panel for displaying images in Swing
 * 
 */
		

import java.awt.Graphics;
import java.awt.Image;
import java.awt.image.BufferedImage;
import javax.swing.JPanel;


public class ImagePanel extends JPanel{
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private BufferedImage image;
	private Image img;
	private boolean isBuffered = true;
	
	public ImagePanel(){
		super();
		image = null;
	}
	public ImagePanel(BufferedImage img){
		super();
		image = img;
	}
	public void setImage(BufferedImage i){
		image = i;
		isBuffered = true;
	}
	public void setImage(Image i){
		img = i;
		isBuffered = false;
	}
	public void paintComponent(Graphics g){
		//use proportions to keep image scale and shape correct(even if window gets resized)
		if(isBuffered){
			if(image != null){
				int width = Math.min(this.getWidth(), image.getWidth());
				int height = Math.min(this.getHeight(), image.getHeight());

				g.drawImage(image,0,0,width,height,null);
			}		
		}
		else{
			if(img != null){
				int width = Math.min(this.getWidth(), img.getWidth(this));
				int height = Math.min(this.getHeight(), img.getHeight(this));

				g.drawImage(img,0,0,width,height,null);
			}	
		}
	}
}
