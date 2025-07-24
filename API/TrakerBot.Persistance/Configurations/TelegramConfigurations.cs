using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using TrakerBot.Core.Entities;

namespace TrakerBot.Persistance.Configurations;

public class TelegramConfiguration : IEntityTypeConfiguration<Telegram>
{
    public void Configure(EntityTypeBuilder<Telegram> builder)
    {
        // Primary Key
        builder.HasKey(t => t.Id);

        // Properties configuration
        builder.Property(t => t.TelegramId)
            .IsRequired()
            .HasMaxLength(50);

        builder.Property(t => t.Username)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(t => t.UserId)
            .IsRequired(false);

        // Relationships
        builder.HasOne(t => t.User)
            .WithMany(u => u.Telegrams)
            .HasForeignKey(t => t.UserId)
            .OnDelete(DeleteBehavior.SetNull);

        // Table configuration
        builder.ToTable("Telegrams");

        // Indexes
        builder.HasIndex(t => t.TelegramId)
            .IsUnique();

        builder.HasIndex(t => t.Username)
            .IsUnique();

        builder.HasIndex(t => t.UserId);
    }
}
