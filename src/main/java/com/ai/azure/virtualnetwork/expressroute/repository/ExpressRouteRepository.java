package com.ai.azure.virtualnetwork.expressroute.repository;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class ExpressRouteRepository {
	private Connection conn;

	public ExpressRouteRepository() {
		try {
			conn = DriverManager.getConnection(
					"jdbc:mysql://localhost:3306/ai_azure_virtualnetwork_expressroute?useSSL=false&allowPublicKeyRetrieval=true",
					"root", "admin" // replace with your MySQL root password
			);
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}

	// Fetch all ExpressRoutes
	public List<String> getAllExpressRoutes() {
		List<String> ers = new ArrayList<>();
		try {
			Statement stmt = conn.createStatement();
			ResultSet rs = stmt.executeQuery("SELECT * FROM expressroutes");
			while (rs.next()) {
				ers.add(rs.getString("name") + " - " + rs.getString("peering_location") + " - "
						+ rs.getString("bandwidth"));
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return ers;
	}

	// Optional: Insert ExpressRoute
	public void insertExpressRoute(String name, String location, String bandwidth) {
		try {
			PreparedStatement pstmt = conn
					.prepareStatement("INSERT INTO expressroutes (name, peering_location, bandwidth) VALUES (?, ?, ?)");
			pstmt.setString(1, name);
			pstmt.setString(2, location);
			pstmt.setString(3, bandwidth);
			pstmt.executeUpdate();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
}
