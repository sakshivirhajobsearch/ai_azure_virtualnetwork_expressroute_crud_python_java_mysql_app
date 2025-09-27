package com.ai.azure.virtualnetwork.expressroute.gui;

import java.awt.BorderLayout;
import java.util.List;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.SwingUtilities;

import com.ai.azure.virtualnetwork.expressroute.repository.ExpressRouteRepository;
import com.ai.azure.virtualnetwork.expressroute.repository.VNetRepository;

public class UnifiedGUI extends JFrame {

	private static final long serialVersionUID = 1L;

	private VNetRepository vnetRepo = new VNetRepository();
	private ExpressRouteRepository erRepo = new ExpressRouteRepository();
	private JTextArea displayArea;

	public UnifiedGUI() {
		setTitle("Azure VNet & ExpressRoute CRUD GUI");
		setSize(600, 500);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		displayArea = new JTextArea();
		JScrollPane scrollPane = new JScrollPane(displayArea);

		JButton fetchVNetBtn = new JButton("Fetch VNets");
		fetchVNetBtn.addActionListener(e -> displayVnets());

		JButton fetchERBtn = new JButton("Fetch ExpressRoutes");
		fetchERBtn.addActionListener(e -> displayExpressRoutes());

		JPanel panel = new JPanel();
		panel.add(fetchVNetBtn);
		panel.add(fetchERBtn);

		add(panel, BorderLayout.NORTH);
		add(scrollPane, BorderLayout.CENTER);
	}

	private void displayVnets() {
		displayArea.setText("");
		List<String> vnets = vnetRepo.getAllVnets();
		for (String vnet : vnets) {
			displayArea.append(vnet + "\n");
		}
	}

	private void displayExpressRoutes() {
		displayArea.setText("");
		List<String> ers = erRepo.getAllExpressRoutes();
		for (String er : ers) {
			displayArea.append(er + "\n");
		}
	}

	public static void main(String[] args) {
		SwingUtilities.invokeLater(() -> {
			UnifiedGUI gui = new UnifiedGUI();
			gui.setVisible(true);
		});
	}
}
