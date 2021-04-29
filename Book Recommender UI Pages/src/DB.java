

import java.io.FileInputStream;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

public class DB {

	private static Connection con = null;
	private static Properties props = new Properties();


	public static Connection getConnection() throws ClassNotFoundException, SQLException {
	    try{
			String DB_DRIVER_CLASS="oracle.jdbc.driver.OracleDriver",
					DB_URL="jdbc:oracle:thin:@DESKTOP-3U1FFEL:1521:XE",
					DB_USERNAME="akshay",
					DB_PASSWORD="akshay";
			
			// load the Driver Class
			Class.forName(DB_DRIVER_CLASS);

			// create the connection now
            con = DriverManager.getConnection(DB_URL,DB_USERNAME,DB_PASSWORD);
	    }
	    catch(Exception e){
	        e.printStackTrace();
	    }
		return con;	
	}
}
