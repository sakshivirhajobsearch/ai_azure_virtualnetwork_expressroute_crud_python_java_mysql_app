package com.ai.azure.virtualnetwork.expressroute.gui;

import java.awt.BorderLayout;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Vector;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTabbedPane;
import javax.swing.JTable;
import javax.swing.SwingUtilities;
import javax.swing.table.DefaultTableModel;

public class UnifiedGUI extends JFrame {

	private static final long serialVersionUID = 1L;

	private JTable vnetTable;
	private JTable expressRouteTable;
	private DefaultTableModel vnetModel;
	private DefaultTableModel erModel;
	private Connection conn;

	public UnifiedGUI() {
		setTitle("AI + Azure Virtual Network & ExpressRoute CRUD");
		setSize(900, 600);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setLayout(new BorderLayout());

		// Initialize DB
		initDBConnection();

		// Tabs
		JTabbedPane tabbedPane = new JTabbedPane();

		// Virtual Network Tab
		JPanel vnetPanel = new JPanel(new BorderLayout());
		vnetModel = new DefaultTableModel(new String[] { "ID", "Name", "Location", "Address Space" }, 0);
		vnetTable = new JTable(vnetModel);
		vnetPanel.add(new JScrollPane(vnetTable), BorderLayout.CENTER);

		JButton refreshVnetBtn = new JButton("Fetch VNets");
		refreshVnetBtn.addActionListener(e -> fetchVirtualNetworks());
		vnetPanel.add(refreshVnetBtn, BorderLayout.SOUTH);

		tabbedPane.add("Virtual Networks", vnetPanel);

		// ExpressRoute Tab
		JPanel erPanel = new JPanel(new BorderLayout());
		erModel = new DefaultTableModel(new String[] { "ID", "Name", "Peering Location", "Bandwidth" }, 0);
		expressRouteTable = new JTable(erModel);
		erPanel.add(new JScrollPane(expressRouteTable), BorderLayout.CENTER);

		JButton refreshErBtn = new JButton("Fetch ExpressRoutes");
		refreshErBtn.addActionListener(e -> fetchExpressRoutes());
		erPanel.add(refreshErBtn, BorderLayout.SOUTH);

		tabbedPane.add("ExpressRoutes", erPanel);

		add(tabbedPane, BorderLayout.CENTER);
	}

	private void initDBConnection() {
		try {
			// Load properties from resources/config.properties
			java.util.Properties props = new java.util.Properties();
			props.load(getClass().getClassLoader().getResourceAsStream("config.properties"));

			String url = "jdbc:mysql://" + props.getProperty("mysql_host") + ":3306/" + props.getProperty("mysql_db")
					+ "?useSSL=false&allowPublicKeyRetrieval=true";
			String user = props.getProperty("mysql_user");
			String password = props.getProperty("mysql_password");

			conn = DriverManager.getConnection(url, user, password);
		} catch (Exception e) {
			JOptionPane.showMessageDialog(this, "DB Connection Failed: " + e.getMessage());
			System.exit(1);
		}
	}

	private void fetchVirtualNetworks() {
		try {
			vnetModel.setRowCount(0);
			Statement stmt = conn.createStatement();
			// Updated table name to 'vnets'
			ResultSet rs = stmt.executeQuery("SELECT * FROM vnets");
			while (rs.next()) {
				Vector<String> row = new Vector<>();
				row.add(String.valueOf(rs.getInt("id")));
				row.add(rs.getString("name"));
				row.add(rs.getString("location"));
				row.add(rs.getString("address_space"));
				vnetModel.addRow(row);
			}
		} catch (SQLException e) {
			JOptionPane.showMessageDialog(this, "Error fetching VNets: " + e.getMessage());
		}
	}

	private void fetchExpressRoutes() {
		try {
			erModel.setRowCount(0);
			Statement stmt = conn.createStatement();
			ResultSet rs = stmt.executeQuery("SELECT * FROM expressroutes");
			while (rs.next()) {
				Vector<String> row = new Vector<>();
				row.add(String.valueOf(rs.getInt("id")));
				row.add(rs.getString("name"));
				row.add(rs.getString("peering_location"));
				row.add(rs.getString("bandwidth"));
				erModel.addRow(row);
			}
		} catch (SQLException e) {
			JOptionPane.showMessageDialog(this, "Error fetching ExpressRoutes: " + e.getMessage());
		}
	}

	public static void main(String[] args) {
		SwingUtilities.invokeLater(() -> {
			UnifiedGUI gui = new UnifiedGUI();
			gui.setVisible(true);
		});
	}
}
