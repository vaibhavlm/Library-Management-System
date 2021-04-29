

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class login
 */
@WebServlet("/login")
public class login extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public login() {
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
		response.setContentType("text/html"); 
		String login_mail=request.getParameter("lmail");
		String login_psw=request.getParameter("lpsw");
		PrintWriter out = response.getWriter();
        try
		{
        	Connection con=DB.getConnection();
        	PreparedStatement ps=con.prepareStatement("select * from USERCREDENTIALS where email=? and password=?");
	        ps.setString(1,login_mail);
	        ps.setString(2,login_psw);
            ResultSet rs = ps.executeQuery();
	        if(rs.next()) {
	        	response.sendRedirect("portal.html");
		    }
	        else
	        {
	        	RequestDispatcher rd= request.getRequestDispatcher("userlogin.html");
	        	rd.include(request, response);
	            out.println("<html>");
	            out.println("<body><center>");
	            out.println("<br><h5 style='color:red;'>Incorrect Username or Password</h5></center></body></html>");
	        }	
	        con.close();
		}
		catch(Exception e)
		{
			System.out.println(e);
		}
		//doGet(request, response);
	}

}
