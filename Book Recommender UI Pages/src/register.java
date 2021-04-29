

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.text.SimpleDateFormat;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class register
 */
@WebServlet("/register")
public class register extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public register() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		String name=request.getParameter("name");
		String mail=request.getParameter("email");
		String dob=request.getParameter("dob").toString();
		String password=request.getParameter("psw");
		PrintWriter out = response.getWriter();
		try {
			java.util.Date date_of_birth = new SimpleDateFormat("yyyy-MM-dd").parse(dob);
			java.sql.Date mySqlDate = new java.sql.Date(date_of_birth.getTime()); 
			Connection con=DB.getConnection();
			PreparedStatement ps1=con.prepareStatement("select * from USERCREDENTIALS where email=?");
	        ps1.setString(1,mail);
	        ResultSet rs = ps1.executeQuery();
	        if(rs.next()) {
	        	RequestDispatcher rd= request.getRequestDispatcher("userlogin.html");
		    	rd.include(request, response);
				out.println("<script>");
				out.println("alert('Registration failed!, Please try with another Email ID');");
				out.println("</script>");
			}
	        else {
		        PreparedStatement ps=con.prepareStatement("insert into USERCREDENTIALS(name,email,date_of_birth,password) values(?,?,?,?)");
		        ps.setString(1,name);
		        ps.setString(2,mail);
		        ps.setDate(3,mySqlDate);
		        ps.setString(4,password);
		        ps.execute();
		        con.close();
		        RequestDispatcher rd= request.getRequestDispatcher("userlogin.html");
		    	rd.include(request, response);
				out.println("<script>");
				out.println("alert('Registered Successfully!');");
				out.println("</script>");
	        }
		}
		catch(Exception e) {
			System.out.println(e);
		}
		//out.println("<body><h1>Successfully Registered</h1></body>");
		//response.sendRedirect("library.html");
	
	}

}
