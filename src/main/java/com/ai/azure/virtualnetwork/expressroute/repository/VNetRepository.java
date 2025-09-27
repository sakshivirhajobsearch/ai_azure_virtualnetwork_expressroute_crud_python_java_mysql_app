package com.ai.azure.virtualnetwork.expressroute.repository;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class VNetRepository {
	
	private Connection conn;

	public VNetRepository() {
		try {
			// Final MySQL connection URL to avoid SSL warning
			conn = DriverManager.getConnection(
					"jdbc:mysql://localhost:3306/ai_azure_virtualnetwork_expressroute?useSSL=false&allowPublicKeyRetrieval=true",
					"root", "admin" // replace with your MySQL root password
			);
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}

	// Fetch all VNets
	public List<String> getAllVnets() {
		List<String> vnets = new ArrayList<>();
		try {
			Statement stmt = conn.createStatement();
			ResultSet rs = stmt.executeQuery("SELECT * FROM vnets");
			while (rs.next()) {
				vnets.add(rs.getString("name") + " - " + rs.getString("location") + " - "
						+ rs.getString("address_space"));
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return vnets;
	}

	// Optional: Insert VNet
	public void insertVnet(String name, String location, String addressSpace) {
		try {
			PreparedStatement pstmt = conn
					.prepareStatement("INSERT INTO vnets (name, location, address_space) VALUES (?, ?, ?)");
			pstmt.setString(1, name);
			pstmt.setString(2, location);
			pstmt.setString(3, addressSpace);
			pstmt.executeUpdate();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
}
