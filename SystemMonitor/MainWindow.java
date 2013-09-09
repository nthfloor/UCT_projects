//class representing main GUI window for system monitor
//Nathan Floor
//FLRNAT001

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTabbedPane;
import javax.swing.JTable;
import javax.swing.JTextArea;
import javax.swing.JTextField;

public class MainWindow extends JFrame implements RefreshData{
	private JTextArea generalSysSpecs;
	private JTextArea memAndCPUOutput;
	private JTextArea otherSystemOutput;
	private JTable processList;
	private JTextField processKillID ;
	
	private MemoryChecker memInfo;
	private CPUChecker cpuInfo;
	private LoadAvgChecker loadavgInfo;
	private UptimeChecker uptimeInfo;
	private ProcessChecker processInfo;
	private CPUusageChecker cpuUsageInfo;
	private boolean refreshTable = true;
	private boolean refreshMem = true;
	private boolean refreshOther = true;
	private float cpuPercent;
	
	public MainWindow(){
		super("System Manager");		
		this.setBounds(50, 50, 800, 500);
		this.setDefaultCloseOperation(EXIT_ON_CLOSE);
		
		//setup JTabbedPane
		JTabbedPane tabs = new JTabbedPane();
		this.add(tabs);
		
		//setup general system output area
		generalSysSpecs = new JTextArea();				
		generalSysSpecs.setEditable(false);
		generalSysSpecs.setBackground(Color.BLACK);
		generalSysSpecs.setForeground(Color.CYAN);		
		JScrollPane generalscrolltext = new JScrollPane(generalSysSpecs);
		generalscrolltext.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
		generalscrolltext.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
		
		//setup other information output area
		otherSystemOutput = new JTextArea();
		otherSystemOutput.setEditable(false);
		otherSystemOutput.setBackground(Color.BLACK);
		otherSystemOutput.setForeground(Color.CYAN);		
		JScrollPane otherscrolltext = new JScrollPane(otherSystemOutput);
		otherscrolltext.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
		otherscrolltext.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
		
		//setup Memory and CPU output area
		memAndCPUOutput = new JTextArea();
		memAndCPUOutput.setEditable(false);
		memAndCPUOutput.setBackground(Color.BLACK);
		memAndCPUOutput.setForeground(Color.CYAN);		
		JScrollPane memAndCPUscrolltext = new JScrollPane(memAndCPUOutput);
		memAndCPUscrolltext.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
		memAndCPUscrolltext.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
		
		JPanel systemInfo = new JPanel();
		systemInfo.setLayout(new GridLayout(3, 1));
		systemInfo.add(generalscrolltext);
		systemInfo.add(otherscrolltext);
		systemInfo.add(memAndCPUscrolltext);		
		tabs.addTab("System Information",null,systemInfo,"displays System info");
		
		//setup process list
		processList = new JTable();
		processList.setEnabled(false);
		processList.setShowGrid(true);	
		processList.setAutoCreateRowSorter(true);
		processList.setBackground(Color.BLACK);
		processList.setForeground(Color.GREEN);
		
		JScrollPane processScrollText = new JScrollPane(processList);
		processScrollText.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);	
		
		//setup kill process functionality
		JButton processKillButton = new JButton("Kill process");
		processKillButton.addActionListener(new ActionListener() {			
			@Override
			public void actionPerformed(ActionEvent a) {
				//execute terminal command
				try{					
					String command = "kill "+processKillID.getText();
					Runtime.getRuntime().exec(command);
					processKillID.setText("");
					processKillID.setFocusable(true);
				}
				catch(Exception e){}
			}
		});
		JLabel processKill = new JLabel("Enter Pid of process to kill:");
		processKillID = new JTextField(30);
		processKillID.setBackground(Color.BLACK);
		processKillID.setForeground(Color.RED);
		JPanel processKillPanel = new JPanel();
		processKillPanel.setLayout(new GridLayout(1,3));
		processKillPanel.add(processKill);
		processKillPanel.add(processKillID);
		processKillPanel.add(processKillButton);
		
		JPanel processPanel = new JPanel();
		processPanel.setLayout(new BorderLayout());
		processPanel.add(processScrollText,BorderLayout.CENTER);
		processPanel.add(processKillPanel,BorderLayout.NORTH);
		
		tabs.addTab("Processes",null,processPanel,"displays process info");
		
		//retrieve computer info and start relevant threads
		processInfo = new ProcessChecker(this);
		processInfo.start();
		
		memInfo = new MemoryChecker(this);
		memInfo.start();
		
		cpuInfo = new CPUChecker();
		cpuInfo.fileReader();
		
		loadavgInfo = new LoadAvgChecker(this);
		loadavgInfo.start();
		
		uptimeInfo = new UptimeChecker(this);
		uptimeInfo.start();
		
		cpuUsageInfo = new CPUusageChecker(this);
		cpuUsageInfo.start();

		displayGeneralInfo();
	}	
	
	//displays general system information
	public void displayGeneralInfo(){
		generalSysSpecs.setText("");
		generalSysSpecs.append("Model: \t\t"+cpuInfo.getModel());
		generalSysSpecs.append("\nCPU MHz: \t\t"+cpuInfo.getCPUSpeed());
		generalSysSpecs.append("\nCache size: \t\t"+cpuInfo.getCacheSize());
		generalSysSpecs.append("\nNumber of Processors: \t"+cpuInfo.getNumProcessors()+"\n");
		generalSysSpecs.append("\nOS Type& Release: \t"+cpuInfo.getOSType());
		generalSysSpecs.append("\nOS Version: \t\t"+cpuInfo.getOSVersion());
		generalSysSpecs.append("\nName of Host: \t"+cpuInfo.getHost());
	}
	
	//displays other system info that continuously updates
	public void displayOtherInfo(){
		otherSystemOutput.setText("");		
		otherSystemOutput.append("\nTotal Processes: \t"+processInfo.getNumProcs());
		otherSystemOutput.append("\nRunning Processes: \t"+processInfo.getNumRunningProcs());
		otherSystemOutput.append("\nZombie Processes: \t"+processInfo.getZombieProcs());
		otherSystemOutput.append("\nLoad Average: \t"+loadavgInfo.getLoadAvg()+"\t(For every 1,5,15 minutes)");
		otherSystemOutput.append("\nUptime: \t\t"+uptimeInfo.getUptime()+"\n");		
	}	
	
	//displays memory and CPU usage including bars as agraphic display
	public void displayMemCPUInfo(){
		memAndCPUOutput.setText("");
		int totMem = memInfo.getTotalMem();
		int freeMem = memInfo.getFreeMem();	
		memAndCPUOutput.append("\nTotal Memory: \t"+totMem+"\tKb");	
		float usedMem = ((totMem-freeMem)/(float)totMem);	
		float freeMemory = (freeMem/(float)totMem);
		String tempMem = "";
		String tempFreeMem = "";
		String tempCPU = "";
		for(int i=0;i < 60;i++){
			//create bar for free memory
			if(i < (int)(60*freeMemory))
				tempFreeMem = tempFreeMem+"|";
			else
				tempFreeMem = tempFreeMem+".";			
			//create bar for used memory
			if(i < (int)(60*usedMem))
				tempMem = tempMem+"|";
			else
				tempMem = tempMem+".";			
			//create bar for CPU usage
			if(i < (int)(60*(cpuPercent/100)))
				tempCPU = tempCPU+"|";
			else
				tempCPU = tempCPU+".";
		}		

		memAndCPUOutput.append("\nFree Memory: \t"+freeMem+"\tKb ["+tempFreeMem+"] "+String.format("%.2f",freeMemory*100)+"%");	
		memAndCPUOutput.append("\nUsed Memory: \t"+(totMem-freeMem)+"\tKb ["+ tempMem + "] " + String.format("%.2f", (usedMem*100)) +"%\n");		
		memAndCPUOutput.append("\nCPU Usage: \t\t\t     ["+tempCPU+"] "+String.format("%.2f", cpuPercent)+"%\n");
	}
	
	//refresh dta being displayed if necessary
	//booleans are used to check if data has been read from files and is ready to be displayed
	public synchronized void paint(Graphics g){	
		if(refreshTable){
			processList.setModel(processInfo.getTableModel());
			refreshTable = false;
		}
		if(refreshOther){
			displayOtherInfo();
			refreshOther = false;
		}
		if(refreshMem){
			displayMemCPUInfo();
			refreshMem = false;
		}
	}

	//interface methods used in the model-view-controller design of the program
	@Override
	public void updateProcess() {
		refreshTable = true;
		repaint();
	}

	@Override
	public void updateMemory() {
		refreshMem = true;
		repaint();
	}

	@Override
	public void updateLoadAvg() {
		refreshOther = true;
		repaint();
	}

	@Override
	public void updateUptime() {
		refreshOther = true;
		repaint();
	}

	@Override
	public void updateCPUUsage(CPUusageChecker percentage) {
		cpuPercent = percentage.percentage;
		refreshMem = true;
		repaint();
	}
}
