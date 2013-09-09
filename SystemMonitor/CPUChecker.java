//retrieves general system information
//note that this class is not a thread as it does not need to update its data continuously
//Nathan Floor
//FLRNAT001

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class CPUChecker {
	private String model;
	private String cpuSpeed;
	private String cacheSize;
	private int numProcessors=0;
	private String osType;
	private String osVersion;
	private String hostName;
	
	//retrieves and formats data
	public void fileReader(){
		try{
			BufferedReader inputstream = new BufferedReader(new FileReader("/proc/cpuinfo"));
			int counter = 0;
			String line = "";
			
			while(line != null){				
				line = inputstream.readLine();	
				if(counter == 4)
					model = line.substring(13).trim();
				else if(counter == 6)
					cpuSpeed = line.substring(10).trim();
				else if(counter == 7)
					cacheSize = line.substring(13).trim();				
				counter++;
				//counts number of processors on PC				
				if((line != null)&&(line.indexOf(":") >= 0))
					if(! line.equals(""))
						if(line.substring(0,9).equals("processor"))
							numProcessors++;									
			}				
			osType = new BufferedReader(new FileReader("/proc/sys/kernel/ostype")).readLine();
			osType = osType+" "+new BufferedReader(new FileReader("/proc/sys/kernel/osrelease")).readLine();
			osVersion = new BufferedReader(new FileReader("/proc/sys/kernel/version")).readLine();
			hostName = new BufferedReader(new FileReader("/proc/sys/kernel/hostname")).readLine();			
			inputstream.close();
		}
		catch(FileNotFoundException e){}
		catch(IOException e){}
	}
	
	//get methods
	public int getNumProcessors(){
		return numProcessors;
	}
	public String getOSType(){
		return osType;
	}
	public String getOSVersion(){
		return osVersion;
	}
	public String getHost(){
		return hostName;
	}
	public String getModel(){
		return model;
	}
	public String getCPUSpeed(){
		return cpuSpeed;
	}
	public String getCacheSize(){
		return cacheSize;
	}
}
